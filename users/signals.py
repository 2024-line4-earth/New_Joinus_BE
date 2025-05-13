from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from share.models import UserMissionState, CardMission
from join.models import Keyword
import random

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_mission(sender, instance, created, **kwargs):
    if created:
        # UserMissionState 생성
        mission_state = UserMissionState.objects.create(user=instance)

        # CardMission 생성 (무작위 키워드)
        random_keyword = random.choice(Keyword.values)
        CardMission.objects.create(mission_state=mission_state, keyword=random_keyword)
