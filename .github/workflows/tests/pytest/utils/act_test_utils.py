import subprocess

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

def test_index_html_present(string: str):
    assert "index.html" in string, "index.html not found in S3 bucket listing"

