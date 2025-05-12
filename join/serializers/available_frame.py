from rest_framework import serializers
from join.models import AvailableFrame

class AvailableFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableFrame
        fields = ["frame_name"]
