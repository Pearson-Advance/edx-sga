from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import default_storage
from openedx.core.djangoapps.site_configuration import helpers
from edx_sga.constants import AWS_S3_FIELDS


class StaffGradedAssignmentStorage:
    def __init__(self):
        aws_s3_bucket = helpers.get_current_site_configuration().get_value("aws_s3_storage_data", '')
        self.aws_s3_storage = None

        if aws_s3_bucket:
            self.check_s3_bucket_keys(aws_s3_bucket)
            self.aws_s3_storage = S3Boto3Storage(
                access_key=aws_s3_bucket.get('aws_s3_access_key'),
                secret_key=aws_s3_bucket.get('aws_s3_secret_key'),
                bucket_name=aws_s3_bucket.get('aws_s3_bucket_name'),
                region_name=aws_s3_bucket.get('aws_s3_region_name')
            )

    def check_s3_bucket_keys(self, settings_dict):
        """
        Method checks integrity and structure of the settings given.
        """
        if not isinstance(settings_dict, dict):
            raise ValueError("Wrong storage settings definition. Expected dict.")

        for aws_s3_field in AWS_S3_FIELDS:
            if aws_s3_field not in settings_dict.keys() or not settings_dict[aws_s3_field]:
                raise ValueError(f"Error on storage settings with field '{aws_s3_field}'.")

        for value, key in settings_dict.items():
            if not value and isinstance(value, str):
                raise ValueError(f"Value error on storage Settings: {key}.")

    def sga_storage(self):
        """
        Returns the storage to be used wheter the default Django's storage or AWS S3 Bucket
        """
        return self.aws_s3_storage if self.aws_s3_storage else default_storage
