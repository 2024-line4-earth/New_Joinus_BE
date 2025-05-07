from .models import MonthlyCardStat

from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date
from rest_framework import status

class TopTwentyView(APIView):
    def get(self, request):
        today = date.today()
        year, month = today.year, today.month

        top_stats = MonthlyCardStat.objects.filter(
            year=year, month=month
        ).select_related('user').order_by('-card_count', 'earliest_created_at')[:20]

        top_20 = [
            {
                "rank": idx,
                "username": stat.user.username,
                "card_count": stat.card_count
            }
            for idx, stat in enumerate(top_stats, start=1)
        ]

        my_stat = MonthlyCardStat.objects.filter(
            user=request.user, year=year, month=month
        ).first()

        all_stats = list(
            MonthlyCardStat.objects.filter(year=year, month=month)
            .order_by('-card_count', 'earliest_created_at')
            .values_list('user_id', flat=True)
        )

        if my_stat:
            my_rank = my_stat.rank
            my_card_count = my_stat.card_count
        else:
            my_rank = len(all_stats) + 1
            my_card_count = 0

        return Response({
            "top_20": top_20,
            "my_rank": my_rank,
            "my_card_count": my_card_count,
        }, status=status.HTTP_200_OK)

