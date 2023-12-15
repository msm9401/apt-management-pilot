import os
from celery import shared_task

from django.conf import settings
from .helpers import MediaBucketMapper


@shared_task
def upload_photo(filename):
    media_bucket_client = MediaBucketMapper(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    media_bucket_client.upload_file_from_tmp(
        settings.AWS_STORAGE_BUCKET_NAME,
        filename,
        f"{settings.AWS_LOCATION}/{filename}",
    )

    os.remove(filename)
