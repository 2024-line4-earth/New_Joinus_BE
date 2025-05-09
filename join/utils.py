from uuid import uuid4
from datetime import datetime, timezone
from constants import ServiceConfigConstants as SCC
import redis # 랭킹앱
from join.models.card_post import CardPost

def build_image_key(user_id: int, ext: str = "jpg") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{SCC.S3_POST_IMAGE_FOLDER_NAME}{ts}_{user_id}-{uuid4()}.{ext}"


r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

# 카드 생성할 때마다 redis 업데이트
def increase_rank_score(user):
    now = datetime.now()
    today = now.date()
    redis_key = f"rank:{now.year}:{now.month}" # 키

    # 하루 3개 초과 시 점수 반영 안 함
    card_count_today = CardPost.objects.filter(user=user, created_at__date=today).count()
    if card_count_today > 3:
        return

    # 점수 증가
    r.zincrby(redis_key, 1, str(user.id))

    # 최초 생성 시간 기록 (동점자 정렬용)
    first_key = f"{redis_key}:first"
    if not r.hexists(first_key, str(user.id)):
        r.hset(first_key, str(user.id), now.timestamp())