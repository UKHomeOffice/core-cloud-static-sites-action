from utils.act_test_utils import verify_s3_headers

def test_verify_file_headers():
    verify_s3_headers("index.html", {
        "ContentType": "text/htmlss",
        "CacheControl": "s-maxage=8640099"
    })