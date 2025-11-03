from utils.act_test_utils import run_act_test

def test_missing_working_directory():
    run_act_test("test-missing-working-directory", "Missing required input: working-directory")