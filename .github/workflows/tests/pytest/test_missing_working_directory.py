from utils.act_test_utils import run_act_workflow, assert_output_contains, get_workflow_logs

def test_missing_working_directory():
    # logs = run_act_workflow("test-missing-working-directory")
    with open("workflow.log") as f:
        logs = f.read()
    assert_output_contains(logs, "Missing required input: working-directory")