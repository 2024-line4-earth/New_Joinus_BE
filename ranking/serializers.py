from rest_framework import serializers

class RankUserSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    username = serializers.CharField()
    card_count = serializers.IntegerField()