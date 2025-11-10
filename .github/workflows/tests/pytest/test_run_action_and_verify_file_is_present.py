from utils.act_test_utils import run_act_workflow, assert_files_exist_in_s3

def test_run_action_and_verify_file_is_present():
    run_act_workflow("test-run-action", expect_failure=False)

    expected_files = [
        "index.html",
        "404.html",
        "500.html",
        "contact/index.html",
        "about/index.html"
    ]
    assert_files_exist_in_s3(expected_files)