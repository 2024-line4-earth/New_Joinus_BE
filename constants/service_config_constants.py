from typing import Final
from django.conf import settings
import os

class ServiceConfigConstants:
    # 비즈니스 로직 전역 상수 모음

    # image 관련 상수
    S3_POST_IMAGE_FOLDER_NAME: Final[str] = settings.AWS_S3_POST_IMAGE_FOLDER_NAME
    PRESIGNED_URL_DURATION_HOUR: Final[int] = int(6)
    LARGE_IMAGE_WIDTH: Final[int] = int(313)
    LARGE_IMAGE_HEIGHT: Final[int] = int(417)
    SMALL_IMAGE_WIDTH: Final[int] = int(169)
    SMALL_IMAGE_HEIGHT: Final[int] = int(225)

    SHAREDCARD_CREATE_POINT: Final[int] = int(50)
    CARDPOST_SHARE_NOTIFIED_POINT: Final[int] = int(20)

    RANK_TOP3_REWARD: Final[int] = int(1000)
    
    RANK_4TO20_REWARD: Final[int] = int(500)

    