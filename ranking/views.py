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
        user_id_str = str(request.user.id)

        # 상위 20위 가져오기
        top_raw = r.zrevrange(redis_key, 0, 19, withscores=True)
        users_data = []
        for rank, (uid, score) in enumerate(top_raw, start=1):
            uid_int = int(uid.decode())
            user = User.objects.filter(id=uid_int).first()
            if user:
                users_data.append({
                    "rank": rank,
                    "username": user.username,
                    "card_count": int(score)
                })

        # 내 순위
        my_rank = r.zrevrank(redis_key, user_id_str)
        my_score = r.zscore(redis_key, user_id_str)

        # redis는 인덱스가 0부터 시작
        if my_rank is not None:
            my_rank = my_rank + 1
        else:
            # Redis에 등록되지 않은 유저 > 꼴찌 등수 부여
            registered_users = r.zcard(redis_key)
            my_rank = registered_users + 1
            my_score = 0
            
        return Response({
            "top_20": users_data,
            "my_rank": my_rank,
            "my_card_count": int(my_score) if my_score else 0
        })

