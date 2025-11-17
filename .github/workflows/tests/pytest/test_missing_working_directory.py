from utils.act_test_utils import run_act_workflow, assert_output_contains, trigger_workflow, fetch_logs

def test_missing_working_directory():
    run_id = trigger_workflow("test-missing-working-directory.yml")
    logs = fetch_logs(run_id)
    assert_output_contains(logs, "Missing required input: working-directory")