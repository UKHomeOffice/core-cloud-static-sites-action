from utils.act_test_utils import run_act_workflow, assert_output_contains

def test_missing_arn():
    logs = run_act_workflow("test-missing-arn")
    assert_output_contains(logs, "Missing required input: assume-role-arn")