import subprocess
import boto3

def run_act_workflow(job_name: str, expect_failure: bool = True) -> str:
    print(f"Running act for job: {job_name}")
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

    print("Exit code:", result.returncode)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    if expect_failure and result.returncode != 1:
        raise AssertionError(f"❌ Expected failure, got exit code {result.returncode}")
    elif not expect_failure and result.returncode != 0:
        raise AssertionError(f"❌ Expected success, got exit code {result.returncode}")

    return result.stdout

def assert_output_contains(string: str, expected_error: str):
    if expected_error not in string:
        raise AssertionError(f"❌ Expected error message '{expected_error}' not found in logs")

    print(f"✅ Output contains expected error: '{expected_error}'")

def assert_test_html_present(string: str):
    assert "test.html" in string, "test.html not found in S3 bucket listing"

def assert_files_exist_in_s3(expected_files: list):
    session = boto3.Session(profile_name='static-site-test')
    s3 = session.client("s3")

    print("Fetching object list from S3 bucket...")
    response = s3.list_objects_v2(Bucket="cc-static-site-staticsite-elliotthrynacz-test-site")
    keys = [obj["Key"] for obj in response.get("Contents", [])]

    print(f"Found {len(keys)} objects in bucket.")
    print(f"Object keys: {keys}")

    missing_files = [f for f in expected_files if f not in keys]
    if missing_files:
        print(f"Missing files: {missing_files}")
    else:
        print("✅ All expected files are present in the S3 bucket.")

    assert not missing_files, f"Missing files in S3 bucket: {missing_files}"
