from django.db import models
from django.conf import settings

class Keyword(models.TextChoices):
    STANDBY_POWER = "STANDBY_POWER", "대기전력"
    RECYCLING     = "RECYCLING",     "재활용"
    SAVING        = "SAVING",        "물절약"
    SEPARATION    = "SEPARATION",    "분리배출"
    REUSABLE      = "REUSABLE",      "다회용기"
    ECO_FRIENDLY  = "ECO_FRIENDLY",  "친환경"
    TUMBLER       = "TUMBLER",       "텀블러"
    CAMPAIGN      = "CAMPAIGN",      "캠페인"
    OTHER         = "OTHER",         "기타"

class CardPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name="card_posts")
    image_key = models.CharField(max_length=150)
    keyword = models.CharField(
        max_length=20,
        choices=Keyword.choices,
        null=False,
        blank=False
    )
    was_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card_post"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"CardPost({self.id}) by {self.user_id} in {self.created_at}"


