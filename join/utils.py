from uuid import uuid4
from datetime import datetime, timezone
from constants import ServiceConfigConstants as SCC

def build_image_key(user_id: int, ext: str = "jpg") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{SCC.S3_POST_IMAGE_FOLDER_NAME}{ts}_{user_id}-{uuid4()}.{ext}"
