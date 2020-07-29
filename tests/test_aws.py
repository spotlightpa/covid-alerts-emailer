import pytest

from definitions import AWS_BUCKET
from src.modules.aws.check_exists_on_s3 import check_exists_on_s3


def test_check_exists_on_s3():
    exists_error_html = check_exists_on_s3(AWS_BUCKET, "error.html")
    assert exists_error_html
    exists_logo = check_exists_on_s3(
        AWS_BUCKET, "assets/logos/banner-black-on-trans-4096.png"
    )
    assert exists_logo
    exists_pony = check_exists_on_s3(AWS_BUCKET, "assets/logos/pony.png")
    assert not exists_pony
