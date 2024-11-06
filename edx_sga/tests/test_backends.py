
import unittest
from unittest.mock import MagicMock, patch
from django.core.files.storage import default_storage
from edx_sga.backends import StaffGradedAssignmentStorage


class StaffGradedAssignmentStorageTest(unittest.TestCase):

    @patch('edx_sga.backends.S3Boto3Storage')
    @patch('edx_sga.backends.helpers')
    def test_returns_s3_storage_storage_settings_given(self, mock_site_helpers, mock_s3_aws_storage):
        """
        Test StaffGradedAssignmentStorage to return a valid S3 storage when the bucket data is given
        """
        storage_settings = {
            'aws_s3_access_key': 'access_key',
            'aws_s3_secret_key': 'secret_key',
            'aws_s3_bucket_name': 'bucket_name',
            'aws_s3_region_name': 'region_name'
        }
        mock_site_configuration = MagicMock()
        mock_site_configuration.get_value.return_value = storage_settings
        mock_site_helpers.get_current_site_configuration.return_value = mock_site_configuration

        xblock_storage = StaffGradedAssignmentStorage().sga_storage()

        mock_s3_aws_storage.assert_called_with(
            access_key='access_key',
            secret_key='secret_key',
            bucket_name='bucket_name',
            region_name='region_name'
        )

        self.assertEqual(xblock_storage, mock_s3_aws_storage.return_value)

    @patch('edx_sga.backends.helpers')
    def test_returns_default_storage_storage_settings_no_given(self, mock_site_helpers):
        """
        Test StaffGradedAssignmentStorage to return the default Django's storage when no settings are defined
        """
        mock_site_configuration = MagicMock()
        mock_site_configuration.get_value.return_value = None
        mock_site_helpers.get_current_site_configuration.return_value = mock_site_configuration

        xblock_storage = StaffGradedAssignmentStorage().sga_storage()
        self.assertEqual(xblock_storage, default_storage)

    @patch('edx_sga.backends.helpers')
    def test_check_s3_bucket_proper_values(self, mock_site_helpers):
        """
        Checks for check_s3_bucket_keys method to check and return the data given in the format expected.
        """
        storage_settings = {
            'aws_s3_access_key': 'access_key',
            'aws_s3_secret_key': 'secret_key',
            'aws_s3_bucket_name': 'bucket_name',
            'aws_s3_region_name': 'region_name'
        }
        mock_site_configuration = MagicMock()
        mock_site_configuration.get_value.return_value = storage_settings
        mock_site_helpers.get_current_site_configuration.return_value = mock_site_configuration

        try:
            xblock_storage_instance = StaffGradedAssignmentStorage()
            xblock_storage_instance.check_s3_bucket_keys(storage_settings)
        except ValueError:
            self.fail('Unexpected raise from check_s3_bucket_keys method.')

    @patch('edx_sga.backends.helpers')
    def test_check_s3_bucket_incomplete_values(self, mock_site_helpers):
        """
        Checks for check_s3_bucket_keys method to raises an exception when the data passed doesn't fullfils the needs.
        """
        storage_settings = {
            'aws_s3_access_key': 'access_key',
            'aws_s3_secret_key': 'secret_key',
        }
        mock_site_configuration = MagicMock()
        mock_site_configuration.get_value.return_value = storage_settings
        mock_site_helpers.get_current_site_configuration.return_value = mock_site_configuration


        with self.assertRaises(ValueError) as exception:
            StaffGradedAssignmentStorage()
        self.assertIn("Error on storage settings with field 'aws_s3_bucket_name'", str(exception.exception))

    @patch('edx_sga.backends.helpers')
    def test_sga_storage_returns_defined_storage(self, mock_site_helpers):
        """
        Test for StaffGradedAssignmentStorage to have assigned the expected storage when the data is passed
        """
        mock_aws_s3_storage = MagicMock(name='MockS3Storage')
        storage_settings = {
            'aws_s3_access_key': 'access_key',
            'aws_s3_secret_key': 'secret_key',
            'aws_s3_bucket_name': 'bucket_name',
            'aws_s3_region_name': 'region_name'
        }
        mock_site_configuration = MagicMock()
        mock_site_configuration.get_value.return_value = storage_settings
        mock_site_helpers.get_current_site_configuration.return_value = mock_site_configuration

        sga_storage_instance = StaffGradedAssignmentStorage()
        sga_storage_instance.aws_s3_storage = mock_aws_s3_storage

        result = sga_storage_instance.sga_storage()
        self.assertEqual(result, mock_aws_s3_storage)

    @patch('edx_sga.backends.default_storage')
    @patch('edx_sga.backends.helpers')
    def test_sga_storage_returns_default_storage(self, mock_site_helpers, mock_default_storage):
        """
        Test for StaffGradedAssignmentStorage to uses the Django's default storage.
        """
        mock_site_configuration = MagicMock()
        mock_site_configuration.get_value.return_value = None
        mock_site_helpers.get_current_site_configuration.return_value = mock_site_configuration

        sga_storage_instance = StaffGradedAssignmentStorage()
        sga_storage_instance.aws_s3_storage = None

        result = sga_storage_instance.sga_storage()
        self.assertEqual(result, mock_default_storage)
