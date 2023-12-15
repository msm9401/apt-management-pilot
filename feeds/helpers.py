import boto3


class MediaBucketMapper:
    def __init__(self, **kwargs):
        params = list(kwargs.keys())
        # assert params.count("endpoint_url")
        assert params.count("aws_access_key_id")
        assert params.count("aws_secret_access_key")
        self.s3_client = boto3.resource(
            "s3",
            # endpoint_url=kwargs.get("endpoint_url"),
            aws_access_key_id=kwargs.get("aws_access_key_id"),
            aws_secret_access_key=kwargs.get("aws_secret_access_key"),
            aws_session_token=None,
            config=boto3.session.Config(signature_version="s3v4"),
            verify=False,
        )

    def upload_file_from_tmp(self, bucket_name, file_name, object_name):
        self.s3_client.meta.client.upload_file(file_name, bucket_name, object_name)
        return
