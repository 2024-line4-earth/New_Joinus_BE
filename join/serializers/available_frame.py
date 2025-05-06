from rest_framework import serializers
from join.models import AvailableFrame


class FrameNameListSerializer(serializers.ListSerializer):
    # many=True 일 때
    def to_representation(self, data):
        # ListSerializer 루프를 건너뛰고 한 번에 변환
        names = data.values_list("frame_name", flat=True)
        return {"frame_names": list(names)}

class AvailableFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableFrame
        fields = ["frame_name"]
        list_serializer_class = FrameNameListSerializer
        