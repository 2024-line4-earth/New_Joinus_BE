from share.models import UserMissionState, CardMission
from join.models import Keyword
import random

def reset_all_missions():
    for state in UserMissionState.objects.all():
        state.is_completed = False
        state.save(update_fields=["is_completed"])

        keyword = random.choice(Keyword.values)
        CardMission.objects.update_or_create(
            mission_state=state,
            defaults={"keyword": keyword}
        )
