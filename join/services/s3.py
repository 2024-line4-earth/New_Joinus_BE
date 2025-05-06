import boto3
from django.conf import settings
from constants import ServiceConfigConstants as SCC

class S3Service:
    # lazily create boto3 client when first used, so Django settings is guaranteed to be ready
    _client = None;
    
    @classmethod
    def _get_client(cls):
        if cls._client is None:
            cls._client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION,
            )
        return cls._client

    @classmethod
    def upload_fileobj(cls, fileobj, key: str, *, content_type: str = "image/jpeg") -> None:
        # 멀티파트로 받은 파일을 S3에 업로드.
        cls._get_client().upload_fileobj(
            fileobj,
            settings.AWS_S3_STORAGE_BUCKET_NAME,
            key,
            ExtraArgs={"ContentType": content_type},
        )

    @classmethod
    def generate_presigned_get_url(cls, key: str, expires: int = SCC.PRESIGNED_URL_DURATION_HOUR * 3600) -> str:
        return cls._get_client().generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": settings.AWS_S3_STORAGE_BUCKET_NAME, "Key": key},
            ExpiresIn=expires,
        )
