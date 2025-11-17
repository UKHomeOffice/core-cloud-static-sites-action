from utils.act_test_utils import trigger_workflow, assert_files_exist_in_s3

def test_verify_files_are_present():
    trigger_workflow("test-run-action.yml")

    expected_files = [
        "index.html",
        "404.html",
        "500.html",
        "contact/index.html",
        "about/index.html"
    ]
    assert_files_exist_in_s3(expected_files)