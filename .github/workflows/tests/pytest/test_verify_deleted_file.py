from utils.act_test_utils import run_act_workflow, create_file, assert_file_in_s3, delete_file

def test_verify_deleted_file():
    create_file("delete.txt")
    run_act_workflow("test-run-action", expect_failure=False)
    assert_file_in_s3("delete.txt", should_exist=True)
    delete_file("delete.txt")
    run_act_workflow("test-run-action", expect_failure=False)
    assert_file_in_s3("delete.txt", should_exist=False)
 