import json
from minio import Minio
from .config import settings, MinioSettings

from structlog import get_logger

log = get_logger()


def init_minio_client(settings: MinioSettings) -> Minio:
    client = Minio(
        settings.endpoint,
        access_key=settings.access_key,
        secret_key=settings.secret_key,
        secure=settings.secure,
    )
    return client


def ensure_buckets(client: Minio, settings: MinioSettings):

    private_bucket = settings.private_bucket
    public_bucket = settings.public_bucket

    if private_bucket:
        if not client.bucket_exists(private_bucket):
            client.make_bucket(private_bucket)
            log.debug(f"✅ Bucket '{private_bucket}' created.")
    if public_bucket:
        if not client.bucket_exists(public_bucket):
            client.make_bucket(public_bucket)
            log.debug(f"✅ Bucket '{public_bucket}' created.")

    # Устанавливаем публичную политику
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{public_bucket}/*"],
            }
        ],
    }
    client.set_bucket_policy(public_bucket, json.dumps(policy))
    log.info("✅ Minio настроенно и готово к работе!!")
