from django.conf import settings
from django.db import models

class CardLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="card_likes",
    )
    sharedcard = models.ForeignKey(
        "share.SharedCard",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "share_cardlike"
        unique_together = ("user", "sharedcard")  # 공유카드마다 1인 최대 1좋아요 가능
