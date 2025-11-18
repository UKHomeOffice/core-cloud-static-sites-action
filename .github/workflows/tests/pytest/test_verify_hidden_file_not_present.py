from utils.act_test_utils import assert_file_in_s3

def test_verify_hidden_file_not_present():
    assert_file_in_s3(".hiddenfile", should_exist=False)