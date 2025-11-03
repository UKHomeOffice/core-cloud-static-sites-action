from utils.act_test_utils import run_act_test

def test_missing_cloudfront_distribution():
    run_act_test("test-missing-cloudfront-distribution", "Missing required input: cloudfront-distribution")