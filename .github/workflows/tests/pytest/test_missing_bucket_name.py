from utils.act_test_utils import run_act_workflow, assert_output_contains

def test_missing_bucket_name():
    logs = run_act_workflow("test-missing-bucket-name")
    assert_output_contains(logs, "Missing required input: bucket-name")