from django.db import models
from django.conf import settings
from join.models.card_post import Keyword

class UserMissionState(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

class CardMission(models.Model):
    mission_state = models.OneToOneField(
        UserMissionState,
        on_delete=models.CASCADE,
    )
    keyword = models.CharField(max_length=30, choices=Keyword.choices)
    updated_at = models.DateTimeField(auto_now=True)
