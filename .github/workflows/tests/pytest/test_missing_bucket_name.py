from utils.act_test_utils import trigger_workflow, assert_output_contains, fetch_logs
import json

def test_missing_bucket_name():
    run_id = trigger_workflow("test-missing-bucket-name.yml", "CCL-763-testing")
    logs = fetch_logs(run_id)

    with open("./expected_errors.json", "r") as f:
        expected_errors = json.load(f)

    assert_output_contains(logs, expected_errors["missing_bucket"])