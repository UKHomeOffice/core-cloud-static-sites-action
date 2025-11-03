import subprocess

def run_act_test(job_name: str, expected_error: str):
    print(f"Running act for job: {job_name}")
    result = subprocess.run(["act", "-j", job_name], capture_output=True, text=True)

    print("Exit code:", result.returncode)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    if result.returncode != 1:
        raise AssertionError(f"❌ Expected failure, got exit code {result.returncode}")

    if expected_error not in result.stdout:
        raise AssertionError(f"❌ Expected error message '{expected_error}' not found in logs")

    print(f"✅ Test passed for job '{job_name}'")