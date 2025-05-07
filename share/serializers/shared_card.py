from rest_framework import serializers
from share.models import SharedCard

class SharedCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SharedCard
        fields = ["id", "user", "cardpost", "description",
                    "is_finalized", "created_at"]
        read_only_fields = ["is_finalized", "created_at"]

class SharedCardFinalizeSerializer(serializers.ModelSerializer):
    """is_finalized 전용 입력"""
    class Meta:
        model = SharedCard
        fields = ["is_finalized"]
