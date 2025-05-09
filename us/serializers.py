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

    class Meta:
        model = Us
        fields = ("username", "my_rank", "current_theme", "points", "daily_message", "total_cards", "available_items")

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
        user_id_str = str(obj.user.id)
        now = datetime.now()
        redis_key = f"rank:{now.year}:{now.month}"

        rank = r.zrevrank(redis_key, user_id_str)

        if rank is not None:
            return rank + 1
        else:
            # 카드를 생성하지 않은 유저 > 꼴찌 등수
            total_ranked = r.zcard(redis_key)
            return total_ranked + 1