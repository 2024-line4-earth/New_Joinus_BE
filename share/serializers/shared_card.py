from rest_framework import serializers
from share.models import SharedCard

class SharedCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SharedCard
        fields = ["id", "user", "cardpost", "description", "created_at"]
        read_only_fields = ["created_at"]
