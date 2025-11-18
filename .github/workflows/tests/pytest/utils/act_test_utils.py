from datetime import datetime, timezone
import json
import subprocess
import hashlib
import boto3
from botocore.exceptions import ClientError 
import logging
import os
import time
import inspect

LOGGER = logging.getLogger(__name__)
bucket_name = "cc-static-site-staticsite-elliotthrynacz-test-site"
folder_path = '.github/workflows/tests/static-site'

def connect_to_s3():
    session = boto3.Session()
    s3 = session.client("s3")
    return s3

def connect_to_cloudfront():
    session = boto3.Session()
    client = session.client("cloudfront")
    return client

def run_act_workflow(job_name: str, expect_failure: bool = True) -> str:
    LOGGER.info(f"Running act for job: {job_name}")
    command = (
        f"act -j {job_name} "
        f"--env-file <(aws configure export-credentials --format env --profile static-site-test) "
        f"--container-architecture linux/amd64"
    )
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=True,
        executable="/bin/bash"
    )

    LOGGER.info("Exit code: %d", result.returncode)
    LOGGER.info("STDOUT:\n%s", result.stdout)
    LOGGER.info("STDERR:\n%s", result.stderr)

    if expect_failure and result.returncode != 1:
        raise AssertionError(f"❌ Expected failure, got exit code {result.returncode}")
    elif not expect_failure and result.returncode != 0:
        raise AssertionError(f"❌ Expected success, got exit code {result.returncode}")

    return result.stdout

def trigger_workflow(workflow_name: str, branch_name: str = "main"):
    test_name = inspect.stack()[1].function
    subprocess.run([
        "gh", "workflow", "run", workflow_name, f"--ref={branch_name}",
        "--field", f"test_name={test_name}"
    ], check=True)

    time.sleep(10)
    run_id = None
    for _ in range(20):  # Increase retries
        result = subprocess.run(
            ["gh", "run", "list", "--workflow", workflow_name, "--json", "databaseId,headBranch,status"],
            capture_output=True, text=True, check=True
        )
        runs = json.loads(result.stdout)
        # Find the run for the correct branch
        for run in runs:
            if run["headBranch"] == branch_name:
                run_id = run["databaseId"]
                break
        if run_id:
            break
        time.sleep(5)

    if not run_id:
        raise RuntimeError(f"Could not find workflow run for {workflow_name} on branch {branch_name}")
    return run_id

def fetch_logs(run_id):
    # Wait until run completes
    for _ in range(30):
        status_result = subprocess.run(
            ["gh", "run", "view", str(run_id), "--json", "status"],
            capture_output=True, text=True, check=True
        )
        status = json.loads(status_result.stdout).get("status")
        if status == "completed":
            break
        time.sleep(5)

    # Fetch logs
    logs_result = subprocess.run(
        ["gh", "run", "view", str(run_id), "--log"],
        capture_output=True, text=True, check=True
    )
    return logs_result.stdout

def assert_output_contains(string: str, expected_error: str):
    if expected_error not in string:
        raise AssertionError(f"❌ Expected error message '{expected_error}' not found in logs: {string}")

    LOGGER.info(f"✅ Output contains expected error: '{expected_error}'")

def assert_file_in_s3(file_key: str, should_exist: bool):
    s3 = connect_to_s3()

    LOGGER.info(f"Checking for {'presence' if should_exist else 'absence'} of file '{file_key}' in S3 bucket...")

    try:
        s3.head_object(Bucket=bucket_name, Key=file_key)
        if should_exist:
            LOGGER.info(f"✅ File '{file_key}' is present in the S3 bucket as expected.")
        else:
            raise AssertionError(f"❌ File '{file_key}' unexpectedly found in S3 bucket")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            if should_exist:
                raise AssertionError(f"❌ File '{file_key}' not found in S3 bucket but was expected.")
            else:
                LOGGER.info(f"✅ File '{file_key}' is not present in the S3 bucket as expected.")
        else:
            LOGGER.error(f"⚠️ Unexpected error when checking file: {e}")
            raise


def assert_files_exist_in_s3(expected_files: list):
    s3 = connect_to_s3()

    LOGGER.info("Fetching object list from S3 bucket...")
    response = s3.list_objects_v2(Bucket=bucket_name)
    keys = [obj["Key"] for obj in response.get("Contents", [])]

    LOGGER.info(f"Found {len(keys)} objects in bucket.")
    LOGGER.info(f"Object keys: {keys}")

    missing_files = [f for f in expected_files if f not in keys]
    if missing_files:
        LOGGER.info(f"Missing files: {missing_files}")
    else:
        LOGGER.info("✅ All expected files are present in the S3 bucket.")

    assert not missing_files, f"Missing files in S3 bucket: {missing_files}"

def assert_file_in_folder(file_name: str, should_exist: bool):
    file_path = os.path.join(folder_path, file_name)
    exists = os.path.isfile(file_path)

    if should_exist and not exists:
        raise AssertionError(f"❌ File '{file_name}' does not exist in folder '{folder_path}' but was expected.")
    elif not should_exist and exists:
        raise AssertionError(f"❌ File '{file_name}' exists in folder '{folder_path}' but should NOT.")
    
    LOGGER.info(f"✅ File '{file_name}' {'exists' if exists else 'does not exist'} in folder '{folder_path}' as expected.")

def validate_latest_invalidation(distribution_id: str, max_age_seconds: int = 60):

    client = connect_to_cloudfront()

    response = client.list_invalidations(DistributionId=distribution_id)
    invalidations = response.get("InvalidationList", {}).get("Items", [])
    if not invalidations:
        raise AssertionError("❌ No invalidations found for this distribution.")

    latest = invalidations[0]
    invalidation_id = latest["Id"]
    create_time = latest["CreateTime"]
    now = datetime.now(timezone.utc)
    age_seconds = (now - create_time).total_seconds()

    LOGGER.info(f"Latest invalidation ID: {invalidation_id}, Status: {latest['Status']}, Age: {age_seconds:.2f}s")

    if age_seconds > max_age_seconds:
        raise AssertionError(f"❌ Latest invalidation is too old ({age_seconds:.2f}s ago).")

    if latest["Status"] not in ["InProgress", "Completed"]:
        raise AssertionError(f"❌ Latest invalidation status is unexpected: {latest['Status']}")

    LOGGER.info("✅ Latest invalidation is recent and in progress or completed.")

def md5_checksum(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()

def verify_file_integrity(file_key: str, local_file_path: str):
    s3 = connect_to_s3()
    s3.download_file(bucket_name, file_key, "/tmp/s3_file")
    s3_md5 = md5_checksum("/tmp/s3_file")
    local_md5 = md5_checksum(local_file_path)

    if s3_md5 != local_md5:
        raise AssertionError(f"❌ Integrity check failed for {file_key}. "
                             f"Local MD5: {local_md5}, S3 MD5: {s3_md5}")
    LOGGER.info("✅ Integrity check passed!")


def verify_s3_headers(file_key: str, expected_headers: dict):
    s3 = connect_to_s3()
    response = s3.head_object(Bucket=bucket_name, Key=file_key)

    mismatches = {}
    for header, expected_value in expected_headers.items():
        actual_value = response.get(header)
        if actual_value != expected_value:
            mismatches[header] = {"expected": expected_value, "actual": actual_value}

    if mismatches:
        raise AssertionError(f"❌ Header check failed: {mismatches}")
    LOGGER.info("✅ Header check passed!")

def test_bucket_permissions():
    s3 = connect_to_s3()
    LOGGER.info(f"Checking bucket ACL and policy for public access: {bucket_name}")

    # Check ACL
    acl = s3.get_bucket_acl(Bucket=bucket_name)
    public_grantees = [
        g for g in acl.get("Grants", [])
        if g.get("Grantee", {}).get("URI") in [
            "http://acs.amazonaws.com/groups/global/AllUsers",
            "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
        ]
    ]
    assert not public_grantees, f"❌ Bucket {bucket_name} ACL allows public access: {public_grantees}"

    # Check bucket policy
    try:
        policy = s3.get_bucket_policy(Bucket=bucket_name)
        policy_doc = json.loads(policy["Policy"])
        for statement in policy_doc.get("Statement", []):
            if statement.get("Effect") == "Allow" and statement.get("Principal") == "*":
                raise AssertionError(f"❌ Bucket {bucket_name} policy allows public access: {statement}")
        LOGGER.info(f"✅ Bucket {bucket_name} policy does not allow public access.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            LOGGER.info("✅ No bucket policy found (as expected).")
        else:
            LOGGER.error(f"⚠️ Unexpected error when checking bucket policy: {e}")
            raise


def get_workflow_logs(workflow_name):
    with open("workflow.log") as f:
        return f.read()
