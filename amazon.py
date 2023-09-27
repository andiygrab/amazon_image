import os
from datetime import datetime

import boto3
import requests
from fastapi import UploadFile, HTTPException

from core.config import settings


s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def generate_s3_key(filename):
    # Generate a unique key based on the current timestamp and the file's original name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_name, extension = os.path.splitext(filename)
    return f"{timestamp}_{base_name}{extension}"


def create_presigned_url(key: str) -> str:
    presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.BUCKET_NAME,
                'Key': key,
            },
            ExpiresIn=300
        )
    return presigned_url


def upload_file_to_bucket(file: UploadFile):
    s3_key = generate_s3_key(file.filename)
    presigned_url = create_presigned_url(s3_key)  # Generate a pre-signed URL for the file
    try:
        # Upload the file to S3 using the pre-signed URL
        with file.file as f:
            response = requests.put(presigned_url, data=f.read())
            response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
    return s3_key


# print(s3_client.list_objects_v2(Bucket=settings.BUCKET_NAME))