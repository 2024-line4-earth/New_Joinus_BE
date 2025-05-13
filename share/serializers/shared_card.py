from rest_framework import serializers
from join.models import CardPost
from join.services import PointService
from join.serializers import CardPostSerializer
from constants import ServiceConfigConstants as SCC
from django.db import IntegrityError
from share.models import (
    SharedCard,
    CardLike,
    PinnedCard,
    StoredCard,
)
class SharedCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cardpost = CardPostSerializer(read_only=True, hide_is_shared=True)
    cardpost_id = serializers.PrimaryKeyRelatedField(
        queryset=CardPost.objects.all(), write_only=True, source="cardpost"
    )
    is_liked = serializers.SerializerMethodField()
    is_pinned = serializers.SerializerMethodField()
    is_stored = serializers.SerializerMethodField()

    class Meta:
        model = SharedCard
        fields = [
            "id",
            "user",
            "cardpost",
            "cardpost_id",
            "description",
            "like_count",
            "is_liked",
            "is_pinned",
            "is_stored",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def __init__(self, *args, **kwargs):
        hide_is_liked = kwargs.pop("hide_is_liked", True)
        hide_is_pinned = kwargs.pop("hide_is_pinned", True)
        hide_is_stored = kwargs.pop("hide_is_stored", True)
        hide_large_image_url = kwargs.pop("hide_large_image_url", False)
        super().__init__(*args, **kwargs)
        if hide_is_liked:
            self.fields.pop("is_liked", None)
        if hide_is_pinned:
            self.fields.pop("is_pinned", None)
        if hide_is_stored:
            self.fields.pop("is_stored", None)
        if hide_large_image_url:
            self.fields["cardpost"] = CardPostSerializer(
                read_only=True,
                hide_is_shared=True,
                hide_large_image_url=hide_large_image_url,
            )
    
    def validate(self, attrs):
        # 현재 로그인한 사용자
        user = self.context["request"].user
        cardpost = attrs.get("cardpost")

        if self.instance is not None:
            return attrs

        if cardpost.user != user:
            raise serializers.ValidationError({"non_field_errors": ["자신이 작성한 카드만 공유(게시) 할 수 있습니다."]})
        return attrs

    def create(self, validated_data):
        try:
            sharedcard = SharedCard.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({"non_field_errors": ["이미 공유된 카드입니다."]})
        
        if not sharedcard.cardpost.was_shared:
            PointService.add(sharedcard.user, SCC.SHAREDCARD_CREATE_POINT, "공유 보상")

        sharedcard.cardpost.was_shared = True
        sharedcard.cardpost.save(update_fields=["was_shared"])
        return sharedcard
    
    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return CardLike.objects.filter(user=user, sharedcard=obj).exists()
    
    def get_is_pinned(self, obj):
        user = self.context["request"].user
        return PinnedCard.objects.filter(user=user, sharedcard=obj).exists()
    
    def get_is_stored(self, obj):
        user = self.context["request"].user
        return StoredCard.objects.filter(user=user, sharedcard=obj).exists()
