from utils.act_test_utils import run_act_workflow, verify_file_integrity

def test_verify_file_integrity():
    verify_file_integrity("index.html", ".github/workflows/tests/static-site/index.html")