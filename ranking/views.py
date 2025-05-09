from users.models import User

import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

class TopTwentyView(APIView):
    def get(self, request):
        now = datetime.now()
        redis_key = f"rank:{now.year}:{now.month}"
        first_key = f"{redis_key}:first"
        user_id_str = str(request.user.id)

        # 점수 기준으로 상위 n명 가져오기
        top_raw = r.zrevrange(redis_key, 0, -1, withscores=True)  # 전체 가져오기

        # 점수 + 최초 생성 시간 기준 정렬
        top_sorted = sorted([
            {
                "user_id": int(uid.decode()),
                "score": int(score),
                "first_ts": float(r.hget(first_key, uid) or 0)
            }
            for uid, score in top_raw
        ], key=lambda x: (-x["score"], x["first_ts"]))

        # 상위 20위 가져오기
        top_20 = top_sorted[:20]
        users_data = []
        for idx, entry in enumerate(top_20, start=1):
            user = User.objects.filter(id=entry["user_id"]).first()
            if user:
                users_data.append({
                    "rank": idx,
                    "username": user.username,
                    "user_id": user.id,
                    "card_count": entry["score"]
                })

        # 내 순위
        my_rank = next((idx + 1 for idx, entry in enumerate(top_sorted)
                        if entry["user_id"] == request.user.id), None)

        my_score = next((entry["score"] for entry in top_sorted
                        if entry["user_id"] == request.user.id), 0)

        if my_rank is None:
            my_rank = len(top_sorted) + 1
            my_score = 0

        return Response({
            "top_20": users_data,
            "my_rank": my_rank,
            "my_card_count": my_score
        })

