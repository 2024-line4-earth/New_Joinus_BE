from rest_framework import serializers
from join.models import CardPost
from share.models import SharedCard
from join.serializers import CardPostSerializer

class SharedCardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    cardpost = CardPostSerializer(read_only=True)
    cardpost_id = serializers.PrimaryKeyRelatedField(
        queryset=CardPost.objects.all(), write_only=True, source="cardpost"
    )
    class Meta:
        model = SharedCard
        fields = ["id", "user", "cardpost", "cardpost_id", "description", "created_at"]
        read_only_fields = ["created_at"]
