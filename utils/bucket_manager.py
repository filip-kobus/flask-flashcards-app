import boto3
import os
from flask import Response
from botocore.config import Config

S3_BUCKET = "flashcards-app-bucket"

s3 = boto3.client("s3",
                  endpoint_url='https://s3.eu-central-1.amazonaws.com')

def upload_to_s3(file, folder, filename):
    """Upload a file to an S3 bucket"""
    object_name = f"{folder}/{filename}"
    
    try:
        s3.upload_fileobj(file, S3_BUCKET, object_name)
        return f"https://{S3_BUCKET}.s3.amazonaws.com/{object_name}"
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return None

def remove_from_s3(folder, filename):
    """Remove a file from S3 bucket"""
    object_name = f"{folder}/{filename}"
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=object_name)
    except Exception as e:
        print(f"Error removing from S3: {e}")
        return None

def get_presigned_url(folder, filename, expiration=3600):
    """Generate a pre-signed URL for the image (valid for 1 hour)."""
    object_name = f"{folder}/{filename}"
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": object_name},
        ExpiresIn=expiration
    )

if __name__=="__main__":
    pass