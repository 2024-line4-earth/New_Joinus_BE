from rest_framework import serializers
from share.models import CardReport

class CardReportSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CardReport
        fields = ["id", "user", "sharedcard", "created_at"]
        read_only_fields = ["created_at"]
