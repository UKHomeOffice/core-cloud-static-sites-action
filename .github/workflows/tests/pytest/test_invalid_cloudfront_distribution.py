from utils.test_utils import trigger_workflow, assert_output_contains, fetch_logs, get_errors

def test_invalid_cloudfront_distribution():
    run_id = trigger_workflow("test-invalid-cloudfront-distribution.yml")
    logs = fetch_logs(run_id)

    expected_errors = get_errors()
    
    assert_output_contains(logs, expected_errors["invalid_cloudfront_distribution"])