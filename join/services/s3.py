from PIL import Image
from io import BytesIO
import boto3
from django.conf import settings
from constants import ServiceConfigConstants as SCC
from join.utils import (
    to_small_key,
    to_large_key,
)

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
    def _resize_image(cls, fileobj, width, height, content_type="image/jpeg"):
        # 이미지 열기 및 리사이즈
        img = Image.open(fileobj)
        img = img.convert("RGB")
        img = img.resize((width, height))

        # 메모리 버퍼에 저장
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)

        return buffer

    @classmethod
    def upload_fileobj_into_small_image(cls, fileobj, key: str, content_type: str = "image/jpeg"):
        small_image_key = to_small_key(key)
        resized_buffer = cls._resize_image(fileobj, SCC.SMALL_IMAGE_WIDTH, SCC.SMALL_IMAGE_HEIGHT, content_type)
        cls._get_client().upload_fileobj(
            resized_buffer,
            settings.AWS_S3_STORAGE_BUCKET_NAME,
            small_image_key,
            ExtraArgs={"ContentType": content_type},
        ) 

    @classmethod
    def upload_fileobj_into_large_image(cls, fileobj, key: str, content_type: str = "image/jpeg"):
        large_image_key = to_large_key(key)
        resized_buffer = cls._resize_image(fileobj, SCC.LARGE_IMAGE_WIDTH, SCC.LARGE_IMAGE_HEIGHT, content_type)

        cls._get_client().upload_fileobj(
            resized_buffer,
            settings.AWS_S3_STORAGE_BUCKET_NAME,
            large_image_key,
            ExtraArgs={"ContentType": content_type},
        ) 

    @classmethod
    def upload_fileobj(cls, fileobj, key: str, *, content_type: str = "image/jpeg") -> None:
        # 멀티파트로 받은 파일을 S3에 업로드.
        cls.upload_fileobj_into_small_image(fileobj, key, content_type)
        cls.upload_fileobj_into_large_image(fileobj, key, content_type)

    @classmethod
    def generate_small_image_presigned_get_url(cls, key: str) -> str:
        small_image_key = to_small_key(key)
        return cls.generate_presigned_get_url(small_image_key)
    
    @classmethod
    def generate_large_image_presigned_get_url(cls, key: str) -> str:
        large_image_key = to_large_key(key)
        return cls.generate_presigned_get_url(large_image_key)

    @classmethod
    def generate_presigned_get_url(cls, key: str, expires: int = SCC.PRESIGNED_URL_DURATION_HOUR * 3600) -> str:
        return cls._get_client().generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": settings.AWS_S3_STORAGE_BUCKET_NAME, "Key": key},
            ExpiresIn=expires,
        )

    @classmethod
    def upload_original_fileobj(cls, fileobj, key: str, content_type: str = "image/png"):
        cls._get_client().upload_fileobj(
            fileobj,
            settings.AWS_S3_STORAGE_BUCKET_NAME,
            key,
            ExtraArgs={"ContentType": content_type},
        )