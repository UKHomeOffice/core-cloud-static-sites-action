from utils.act_test_utils import run_act_workflow, validate_latest_invalidation

def test_verify_cloudfront_invalidation_success():
    run_act_workflow("test-run-action", expect_failure=False)
    validate_latest_invalidation("E39K1BO4OKXJ30")

 