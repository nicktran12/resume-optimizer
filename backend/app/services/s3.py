import boto3
from botocore.exceptions import ClientError

from app.core.config import get_settings

settings = get_settings()

_s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

def _object_key(resume_id: str) -> str:
    return f"resumes/{resume_id}/original.pdf"

def upload_resume(resume_id: str, file_bytes: bytes) -> str:
    key = _object_key(resume_id)
    _s3_client.put_object(
        Bucket=settings.S3_BUCKET,
        Key=key,
        Body=file_bytes,
        ContentType="application/pdf",
    )
    return key

def download_resume(resume_id: str) -> bytes:
    key = _object_key(resume_id)
    try:
        response = _s3_client.get_object(Bucket=settings.S3_BUCKET, Key=key)
        return response["Body"].read()
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            raise FileNotFoundError(f"No resume found in S3 for resume_id={resume_id}") from e
        raise

def delete_resume(resume_id: str) -> None:
    key = _object_key(resume_id)
    _s3_client.delete_object(Bucket=settings.S3_BUCKET, Key=key)