"""Presigned R2 URLs for the per-course data bundles."""

import os

import boto3
from botocore.config import Config

VALID_COURSES = {f"course-{n:02d}" for n in range(2, 22)}
URL_TTL_SECONDS = 600


def _client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


def presigned_url(course_id: str) -> tuple[str, str]:
    """Returns (url, sha256). The checksum comes from object metadata set
    at upload time by the bundle splitter; empty string when absent."""
    client = _client()
    bucket = os.environ.get("R2_BUCKET", "u2xai-course-bundles")
    object_key = f"bundles/{course_id}.zip"
    head = client.head_object(Bucket=bucket, Key=object_key)
    sha256 = head.get("Metadata", {}).get("sha256", "")
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": object_key},
        ExpiresIn=URL_TTL_SECONDS,
    )
    return url, sha256
