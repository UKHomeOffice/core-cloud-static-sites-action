from utils.act_test_utils import run_act_test

def test_missing_bucket_name():
    run_act_test("test-missing-bucket-name", "Missing required input: bucket-name")