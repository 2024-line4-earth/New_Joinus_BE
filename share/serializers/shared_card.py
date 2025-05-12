from rest_framework import serializers
from join.models import CardPost
from join.services import PointService
from share.models import SharedCard
from join.serializers import CardPostSerializer
from constants import ServiceConfigConstants as SCC

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

    def create(self, validated_data):
        shared_card = SharedCard.objects.create(**validated_data)
        PointService.add(shared_card.user, SCC.SHAREDCARD_CREATE_POINT, "공유 보상")
        return shared_card
    