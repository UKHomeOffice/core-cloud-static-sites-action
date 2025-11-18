from utils.act_test_utils import trigger_workflow, assert_output_contains, fetch_logs

def test_invalid_cloudfront_distribution():
    run_id = trigger_workflow("test-invalid-cloudfront-distribution.yml", "CCL-763-testing")
    logs = fetch_logs(run_id)
    assert_output_contains(logs, "An error occurred (AccessDenied) when calling the CreateInvalidation operation")