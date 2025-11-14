from utils.act_test_utils import run_act_workflow, assert_cache_control_header

def test_verify_cache_control():
    assert_cache_control_header("index.html", "86400")