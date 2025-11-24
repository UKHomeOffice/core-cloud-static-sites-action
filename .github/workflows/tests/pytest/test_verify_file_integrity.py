from utils.test_utils import verify_file_integrity

def test_verify_file_integrity():
    verify_file_integrity("index.html", ".github/workflows/tests/static-site/index.html")