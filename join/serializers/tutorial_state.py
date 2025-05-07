from rest_framework import serializers
from join.models import UserTutorialState
from join.services import PointService
from constants import ServiceConfigConstants as SCC

class UserTutorialStateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserTutorialState
        fields = ["tutorial_completed"]

    def update(self, instance, validated_data):
        if not instance.tutorial_completed and validated_data.get("tutorial_completed"):
            PointService.add(instance.user, SCC.TUTORIAL_COMPLETED_POINT, "튜토리얼 완료")
        return super().update(instance, validated_data)
    