from utils.act_test_utils import trigger_workflow, assert_output_contains, fetch_logs

def test_missing_bucket_name():
    run_id = trigger_workflow("test-missing-bucket-name.yml", "CCL-763-testing")
    logs = fetch_logs(run_id)
    assert_output_contains(logs, "Missing required input: bucket-name")