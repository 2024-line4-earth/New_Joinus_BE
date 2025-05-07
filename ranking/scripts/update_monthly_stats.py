import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newjoinus.settings.local')
django.setup()

# ~7까지의 코드는 맨 위에 위치해야 함. 안 그럼 모듈 못 찾음
from join.models.card_post import CardPost
from ranking.models import MonthlyCardStat
from datetime import datetime, timedelta, date
from collections import defaultdict
from django.db.models import Min, Count

def monthly_stats():
    print("== monthly_stats 실행 ==")
    today = date.today()

    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)

    start_dt = datetime.combine(start_of_month, datetime.min.time())
    end_dt = datetime.combine(end_of_month, datetime.min.time())

    daily_counts = (
        CardPost.objects.filter(created_at__range=(start_dt, end_dt))
        .values('user_id', 'created_at__date')
        .annotate(count=Count('id'), earliest=Min('created_at'))
    )

    monthly_totals = defaultdict(lambda: {'count': 0, 'earliest': None})

    for record in daily_counts:
        limited_count = min(record['count'], 3)
        user_id = record['user_id']
        monthly_totals[user_id]['count'] += limited_count
        if not monthly_totals[user_id]['earliest'] or record['earliest'] < monthly_totals[user_id]['earliest']:
            monthly_totals[user_id]['earliest'] = record['earliest']

    sorted_stats = sorted(monthly_totals.items(), key=lambda x: (-x[1]['count'], x[1]['earliest']))
    for idx, (user_id, data) in enumerate(sorted_stats, start=1):
        MonthlyCardStat.objects.update_or_create(
            user_id=user_id,
            year=today.year,
            month=today.month,
            defaults={
                'card_count': data['count'],
                'earliest_created_at': data['earliest'],
                'rank': idx
            }
        )

if __name__ == "__main__":
    monthly_stats()