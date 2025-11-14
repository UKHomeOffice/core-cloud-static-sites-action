from utils.act_test_utils import run_act_workflow, assert_output_contains

def test_invalid_cloudfront_distribution():
    logs = run_act_workflow("test-invalid-cloudfront-distribution", expect_failure=True)
    assert_output_contains(logs, "An error occurred (AccessDenied) when calling the CreateInvalidation operation")