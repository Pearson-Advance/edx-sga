"""
Tests for SGA utility functions
"""
from unittest.mock import patch
from django.core.files.storage import default_storage
import pytest
import pytz
from storages.backends.s3boto3 import S3Boto3Storage

from edx_sga.tests.common import is_near_now
from edx_sga.utils import get_default_storage, is_finalized_submission, utcnow


@pytest.mark.parametrize(
    "submission_data,expected_value",
    [
        ({"answer": {"finalized": True}}, True),
        ({"answer": {"filename": "file.txt"}}, True),
        ({"answer": {}}, True),
        ({"answer": {"finalized": False}}, False),
        ({"answer": None}, False),
        ({}, False),
    ],
)
def test_is_finalized_submission(submission_data, expected_value):
    """Test for is_finalized_submission"""
    assert is_finalized_submission(submission_data) is expected_value


def test_utcnow():
    """
    tznow should return a datetime object in UTC
    """
    now = utcnow()
    assert is_near_now(now)
    assert now.tzinfo.zone == pytz.utc.zone

patch("edx_sga.utils.configuration_helpers")
def test_get_default_storage_with_settings_override(mock_configuration_helpers):
    """
    get_default_storage should return an S3Boto3Storage object
    """
    mock_configuration_helpers.return_value.get_value.return_value = (
        {
            "SGA_STORAGE_SETTINGS": {
                "STORAGE_CLASS": "storages.backends.s3boto3.S3Boto3Storage",
                "STORAGE_KWARGS": {
                    "access_key": "test_key",
                    "secret_key": "test_secret",
                    "bucket_name": "test-bucket-1",
                    "region_name": "us-east-1",
                },
            },
        },
    )
    storage = get_default_storage()
    assert storage.__class__ == S3Boto3Storage
    # make sure kwargs are passed through constructor
    assert storage.bucket.name == 'test'

patch("edx_sga.utils.configuration_helpers")
def test_get_default_storage_without_settings_override(mock_configuration_helpers):
    """
    get_default_storage should return default_storage object
    """
    mock_configuration_helpers.return_value.get_value.return_value = {}
    storage = get_default_storage()
    assert storage == default_storage
