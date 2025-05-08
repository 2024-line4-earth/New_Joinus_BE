from rest_framework import serializers
from .models import MonthlyCardStat

class RankUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = MonthlyCardStat
        fields = ['username', 'card_count']