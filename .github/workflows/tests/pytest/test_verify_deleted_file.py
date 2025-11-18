from utils.act_test_utils import trigger_workflow, create_file, assert_file_in_s3, delete_file

def test_verify_deleted_file():
    create_file("delete.txt")
    trigger_workflow("test-run-action.yml", "CCL-763-testing")
    assert_file_in_s3("delete.txt", should_exist=True)
    delete_file("delete.txt")
    trigger_workflow("test-run-action.yml", "CCL-763-testing")
    assert_file_in_s3("delete.txt", should_exist=False)
 