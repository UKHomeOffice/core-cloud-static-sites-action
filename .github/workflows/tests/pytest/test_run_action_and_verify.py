from utils.act_test_utils import run_act_workflow, test_index_html_present

def test_run_action_and_verify():
    logs = run_act_workflow("test-run-action-and-verify", expect_failure=False)
    test_index_html_present(logs)