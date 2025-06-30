import random
from django.db import transaction
from django.utils.timezone import now
from join.models.card_post import Keyword
from share.models import UserMissionState, CardMission


@transaction.atomic
def get_or_refresh_mission(user):
    state, _ = (
        UserMissionState.objects
        .select_for_update()
        .get_or_create(user=user)
    )

    mission, _ = (
        CardMission.objects
        .select_for_update()
        .get_or_create(
            mission_state=state,
            defaults={"keyword": random.choice(Keyword.values)},
        )
    )

    # 날짜가 바뀐 경우: 상태 초기화 + 키워드 재추첨
    today = now()
    if state.updated_at.date() != today.date():
        # 상태 초기화
        state.is_completed = False
        state.save(update_fields=["is_completed", "updated_at"])

        # 키워드 재추첨
        mission.keyword = random.choice(Keyword.values)
        mission.save(update_fields=["keyword", "updated_at"])

    return state, mission
