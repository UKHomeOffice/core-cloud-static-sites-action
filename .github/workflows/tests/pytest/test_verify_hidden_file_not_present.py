from utils.act_test_utils import run_act_workflow, assert_file_in_s3

def test_verify_hidden_file_not_present():
    run_act_workflow("test-run-action", expect_failure=False)
    assert_file_in_s3(".hiddenfile", should_exist=False)