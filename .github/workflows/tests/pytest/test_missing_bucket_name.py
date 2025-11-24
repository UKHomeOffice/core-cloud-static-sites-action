from utils.act_test_utils import trigger_workflow, assert_output_contains, fetch_logs
import json
import os

def test_missing_bucket_name():
    run_id = trigger_workflow("test-missing-bucket-name.yml", "CCL-763-testing")
    logs = fetch_logs(run_id)

    file_path = os.path.join(os.path.dirname(__file__), "expected_errors.json")

    with open(file_path, "r") as f:
        expected_errors = json.load(f)

    assert_output_contains(logs, expected_errors["missing_bucket"])