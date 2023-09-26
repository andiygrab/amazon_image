import os
from datetime import datetime

import boto3
from fastapi import UploadFile

from core.config import settings


s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def generate_s3_key(filename):
    # Generate a unique key based on the current timestamp and the file's original name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_name, extension = os.path.splitext(filename)
    return f"{timestamp}_{base_name}{extension}"


def upload_file_to_bucket(file: UploadFile):
    s3_key = generate_s3_key(file.filename)

    # Upload the file to S3
    s3_client.upload_fileobj(
        file.file,
        settings.BUCKET_NAME,
        s3_key
    )
    return s3_key
