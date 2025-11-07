from utils.act_test_utils import run_act_workflow, assert_output_contains

def test_missing_cloudfront_distribution():
    logs = run_act_workflow("test-missing-cloudfront-distribution")
    assert_output_contains(logs, "Missing required input: cloudfront-distribution")