from utils.act_test_utils import run_act_test

def test_missing_arn():
    run_act_test("test-missing-arn", "Missing required input: assume-role-arn")