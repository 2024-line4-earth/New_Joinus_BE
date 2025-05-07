from django.conf import settings
from django.db import models

class CardReport(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="card_reports",
    )
    sharedcard = models.ForeignKey(
        "share.SharedCard",
        on_delete=models.CASCADE,
        related_name="reports",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "share_cardreport"
