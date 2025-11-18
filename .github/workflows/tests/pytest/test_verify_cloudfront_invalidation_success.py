from utils.act_test_utils import trigger_workflow, validate_latest_invalidation

def test_verify_cloudfront_invalidation_success():
    trigger_workflow("test-run-action.yml")
    validate_latest_invalidation("E39K1BO4OKXJ30")