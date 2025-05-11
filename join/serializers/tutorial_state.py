from rest_framework import serializers
from join.models import UserTutorialState
from join.services import PointService
from constants import ServiceConfigConstants as SCC

class UserTutorialStateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserTutorialState
        fields = ["tutorial_completed"]

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    