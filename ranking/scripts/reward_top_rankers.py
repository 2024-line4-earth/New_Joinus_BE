import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newjoinus.settings.local')
django.setup()

from constants.service_config_constants import ServiceConfigConstants as SCC
from ranking.models import MonthlyCardStat
from join.services.points import PointService

def reward_top_rankers():
    now = datetime.now()

    # 전달 랭킹에 대해 지급. push 할 때-1 추가 해야 함
    year = now.year
    month = now.month
    if month == 0:
        year -= 1
        month = 12

    print(f"== {year}년 {month}월 랭킹 보상 지급 시작 ==")

    top_stats = MonthlyCardStat.objects.filter(
        year=year, month=month
    ).select_related('user').order_by('rank')  # rank 기준 오름차순

    for stat in top_stats:
        if stat.rank is None:
            continue

        # 생성한 카드가 없는 경우 제외
        if stat.card_count == 0:
            print(f"{stat.rank}위 - {stat.user.username} 카드 없음, 지급 제외")
            continue

        if stat.rank <= 3:
            reward = SCC.RANK_TOP3_REWARD
        elif stat.rank <= 20:
            reward = SCC.RANK_4TO20_REWARD
        else:
            continue 

        user = stat.user

        description = f"{year}년 {month}월 랭킹 {stat.rank}위 보상"
        PointService.add(user=user, amount=reward, msg=description)

        print(f"{stat.rank}위 - {user.username} → {reward}포인트 지급 완료")

    print("=== 보상 지급 완료 ===")

if __name__ == "__main__":
    reward_top_rankers()
