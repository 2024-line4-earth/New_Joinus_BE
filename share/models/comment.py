from django.conf import settings
from django.db import models

class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="share_comments",
    )
    sharedcard = models.ForeignKey(
        "share.SharedCard",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "share_comment"
        ordering = ["created_at"]
