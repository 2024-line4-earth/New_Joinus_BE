from rest_framework import serializers
from share.models import CardLike

class CardLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CardLike
        fields = ["id", "user", "sharedcard", "created_at"]
        read_only_fields = ["created_at"]
