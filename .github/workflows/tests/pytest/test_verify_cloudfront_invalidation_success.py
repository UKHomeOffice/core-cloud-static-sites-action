from utils.test_utils import trigger_workflow, validate_latest_invalidation, wait_for_workflow

def test_verify_cloudfront_invalidation_success():
    run_id = trigger_workflow("test-run-action.yml", "CCL-763-testing")
    wait_for_workflow(run_id)
    validate_latest_invalidation("E39K1BO4OKXJ30")