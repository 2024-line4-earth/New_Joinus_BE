from rest_framework import serializers
from join.models import CardPost
from join.services import PointService
from share.models import SharedCard
from join.serializers import CardPostSerializer
from constants import ServiceConfigConstants as SCC
from django.db import IntegrityError

class SharedCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cardpost = CardPostSerializer(read_only=True, hide_is_shared=True)
    cardpost_id = serializers.PrimaryKeyRelatedField(
        queryset=CardPost.objects.all(), write_only=True, source="cardpost"
    )
    class Meta:
        model = SharedCard
        fields = ["id", "user", "cardpost", "cardpost_id", "description", "created_at"]
        read_only_fields = ["created_at"]

    def validate(self, attrs):
        # 현재 로그인한 사용자
        user = self.context["request"].user
        cardpost = attrs.get("cardpost")

        if cardpost.user != user:
            raise serializers.ValidationError({"non_field_errors": ["자신이 작성한 카드만 공유(게시) 할 수 있습니다."]})
        return attrs

    def create(self, validated_data):
        try:
            shared_card = SharedCard.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"non_field_errors": ["이미 공유된 카드입니다."]})
        
        if not shared_card.cardpost.was_shared:
            PointService.add(shared_card.user, SCC.SHAREDCARD_CREATE_POINT, "공유 보상")

        shared_card.cardpost.was_shared = True
        shared_card.cardpost.save(update_fields=["was_shared"])
        return shared_card
    