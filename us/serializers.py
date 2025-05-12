from rest_framework import serializers
from .models import *
from market.models import Item, Purchase
from market.serializers import ItemListSerializer
from join.models.card_post import CardPost

import redis
from datetime import datetime

r = redis.StrictRedis(host="127.0.0.1", port=6379, db=0)

class UsSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    points = serializers.IntegerField(source='user.points', read_only=True)
    available_items = serializers.SerializerMethodField()
    current_theme = serializers.ReadOnlyField(source='user.current_theme')
    daily_message = serializers.SerializerMethodField()
    total_cards = serializers.SerializerMethodField()
    my_rank = serializers.SerializerMethodField()
    step = serializers.SerializerMethodField()

    class Meta:
        model = Us
        fields = ("username", "my_rank", "current_theme", "points", "step", "daily_message", "total_cards", "available_items")

    # 총 누적 카드 개수
    def get_total_cards(self, obj):
        return CardPost.objects.filter(user=obj.user).count()

    # 마켓에서 구매 가능한 아이템
    def get_available_items(self, obj):
        user = obj.user
        user_points = user.points

        # 사용자가 이미 구매한 아이템 목록
        purchased_ids = Purchase.objects.filter(user=user).values_list('item__id', flat=True)
        items_not_purchased = Item.objects.exclude(id__in=purchased_ids)

        # 구매하지 않은 아이템 중 최대 4개
        buyable_items = items_not_purchased.filter(price__lte=user_points)[:4]

        return ItemListSerializer(buyable_items, many=True).data
    
    # 데일리 메세지
    def get_daily_message(self, obj):
        from datetime import date
        today = date.today()
        selected = SelectedDailyMessage.objects.filter(date=today).first()
        return selected.message.content if selected else "당신이 있어서 세상이 더 아름다워요"

    # 순위 구하기
    def get_my_rank(self, obj):
        now = datetime.now()
        redis_key = f"rank:{now.year}:{now.month}"
        first_key = f"{redis_key}:first"
        user_id_str = str(obj.user.id)

        # 전체 랭킹 불러오기
        rankings = r.zrevrange(redis_key, 0, -1, withscores=True)

        sorted_users = sorted([
            {
                "user_id": int(uid.decode()),
                "score": int(score),
                "first_ts": float(r.hget(first_key, uid.decode()) or 0)
            }
            for uid, score in rankings
        ], key=lambda x: (-x["score"], x["first_ts"]))  # 점수 내림차순, 먼저 만든 시간 오름차순

        for idx, user in enumerate(sorted_users, start=1):
            if user["user_id"] == obj.user.id:
                return idx

        # redis에 없는 유저는 꼴찌
        return len(sorted_users) + 1
    
    # 스텝(막대기바) 구하기
    def get_step(self, obj):
        total = CardPost.objects.filter(user=obj.user).count()

        if total == 0:
            return 0
        return (total - 1) % 4 + 1
