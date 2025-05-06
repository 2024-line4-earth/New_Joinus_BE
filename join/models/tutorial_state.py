from django.db import models
from django.conf import settings

class UserTutorialState(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name="tutorial_state")
    tutorial_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "user_tutorial_state"

    def __str__(self):
        return f"TutorialState({self.user_id}): {self.tutorial_completed}"
