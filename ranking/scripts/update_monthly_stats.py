import os
import sys
import django
import redis

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newjoinus.settings.local')
django.setup()
# redis 제외 여기까지의 코드는 맨 위에 위치해야 함. 안 그럼 모듈 못 찾음

from users.models import User
from ranking.models import MonthlyCardStat
from datetime import datetime

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

def monthly_stats():
    print("== Redis → DB 랭킹 저장 실행 ==")
    now = datetime.now()
    year, month = now.year, now.month
    redis_key = f"rank:{year}:{month}"
    first_key = f"{redis_key}:first" # 사진 생성 날짜

    rankings = r.zrevrange(redis_key, 0, -1, withscores=True)

    sorted_users = sorted([
        {
            "user_id": int(uid.decode()),
            "score": int(score),
            "first_ts": float(r.hget(first_key, uid.decode()) or 0)
        }
        for uid, score in rankings
    ], key=lambda x: (-x["score"], x["first_ts"]))

    for idx, user in enumerate(sorted_users, start=1):
        MonthlyCardStat.objects.update_or_create(
            user_id=user["user_id"],
            year=year,
            month=month,
            defaults={
                "card_count": user["score"],
                "earliest_created_at": datetime.fromtimestamp(user["first_ts"]),
                "rank": idx
            }
        )


if __name__ == "__main__":
    monthly_stats()