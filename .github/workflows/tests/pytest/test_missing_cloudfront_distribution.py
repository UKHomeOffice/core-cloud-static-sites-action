from utils.act_test_utils import trigger_workflow, assert_output_contains, fetch_logs

def test_missing_cloudfront_distribution():
    run_id = trigger_workflow("test-missing-cloudfront-distribution.yml", "chrismessabout2")
    logs = fetch_logs(run_id)
    assert_output_contains(logs, "Missing required input: cloudfront-distribution")