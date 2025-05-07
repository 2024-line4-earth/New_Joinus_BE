from typing import Final
from django.conf import settings
import os

class ServiceConfigConstants:
    # 비즈니스 로직 전역 상수 모음

    S3_POST_IMAGE_FOLDER_NAME: Final[str] = settings.AWS_S3_POST_IMAGE_FOLDER_NAME

    PRESIGNED_URL_DURATION_HOUR: Final[int] = int(6)

    CARDPOST_CREATE_POINT: Final[int] = int(100)

    TUTORIAL_COMPLETED_POINT: Final[int] = int(500)
