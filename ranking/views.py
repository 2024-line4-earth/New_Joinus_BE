from users.models import User
from share.pagination import SharedCardCursorPagination
from share.models import SharedCard
from share.serializers.shared_card import SharedCardSerializer
from .models import NotificationStatus

import redis
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from rest_framework.generics import get_object_or_404
from rest_framework import status

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

class TopTwentyView(APIView):
    permission_classes = [IsAuthenticated]

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
        
        my_username = request.user.username

        if my_rank is None:
            my_rank = len(top_sorted) + 1
            my_score = 0

        # 유의사항 확인 true/false
        notif, _ = NotificationStatus.objects.get_or_create(user=request.user)

        return Response({
            "top_20": users_data,
            "my_rank": my_rank,
            "my_username": my_username,
            "my_card_count": my_score,
            "notification": notif.seen
        }, status=status.HTTP_200_OK)

# 상위 20위 유저의 공유 글 리스트
class RankUserSharedCardView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = SharedCardCursorPagination

    def get(self, request, user_id):
        query_user = get_object_or_404(User, id=user_id)
        query_params = request.query_params

        only_this_month = query_params.get("only_this_month", "false").lower() == "true"
        order = query_params.get("order", "recent")

        queryset = SharedCard.objects.filter(user=query_user).select_related("cardpost")

        if only_this_month:
            today = now()
            queryset = queryset.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )

        if order == "likes":
            queryset = queryset.order_by("-like_count", "-created_at")
        else:
            queryset = queryset.order_by("-created_at")

        # 순위 계산
        now_ = datetime.now()
        redis_key = f"rank:{now_.year}:{now_.month}"
        first_key = f"{redis_key}:first"

        top_raw = r.zrevrange(redis_key, 0, -1, withscores=True)
        top_sorted = sorted([
            {
                "user_id": int(uid.decode()),
                "score": int(score),
                "first_ts": float(r.hget(first_key, uid) or 0)
            }
            for uid, score in top_raw
        ], key=lambda x: (-x["score"], x["first_ts"]))

        rank = next((idx + 1 for idx, entry in enumerate(top_sorted)
                        if entry["user_id"] == query_user.id), None)

        if rank is None:
            rank = len(top_sorted) + 1

        username = query_user.username

        # 페이징 처리
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = SharedCardSerializer(
            page,
            many=True,
            context={"request": request},
            hide_large_image_url=True,
            hide_is_liked=True,
            hide_is_pinned=True,
        )
        
        return paginator.get_paginated_response({
            "rank": rank, 
            "username": username,
            "sharedcards": serializer.data})
    
# 첫번째 유의사항
class NotificationOneView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notif, _ = NotificationStatus.objects.get_or_create(user=request.user)
        notif.seen = True
        notif.save()
        return Response({"normal_message": """조인어스의 랭킹은 매달 가장 많은 실천카드를 만든 사람 순으로 순위가 매겨집니다.
집계는 하루에 최대 3개로 제한되며, 31일인 달일 경우 최대 93개까지 집계가 됩니다.
또한 만든 시간의 순서가 빠를수록 집계가 우선적으로 되어 먼저 최대치의 실천카드를 만든 사람의 랭킹이 더 위로 올라가게 됩니다.""",
                        "red_message": """*1등도 93개, 2등도 93개인 경우, 1등이 93개의 실천카드를 먼저 채운 것입니다.
*랭킹은 매달 새롭게 갱신됩니다."""}, status=status.HTTP_200_OK)

# 두번째 유의사항
class NotificationTwoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": """다 읽으셨나요?
핵심을 다시 정리하자면
• 매달 갱신되는 랭킹
• 실천카드를 많이 만든 순으로 순위 지정
• 하루에 최대 3개까지
• 먼저 만든 사람이 우선
기억해주세요~!"""}, status=status.HTTP_200_OK)
    
# 세번째 유의사항
class NotificationThreeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "매 달 마지막 날 집계가 끝난 이후 랭킹 1, 2, 3위는 1000P 4~20위는 500P가 지급됩니다!"}
                        , status=status.HTTP_200_OK)
