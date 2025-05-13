from rest_framework import serializers
from share.models import PinnedCard

class PinnedSharedCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PinnedCard
        fields = ["id", "user", "sharedcard", "created_at"]
        read_only_fields = ["created_at"]
