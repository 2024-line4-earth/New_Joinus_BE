from rest_framework import serializers
from share.models import StoredCard

class StoredCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = StoredCard
        fields = ["id", "user", "sharedcard", "created_at"]
        read_only_fields = ["created_at"]
        