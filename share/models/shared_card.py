from django.conf import settings
from django.db import models

class SharedCard(models.Model):
    # 사용자가 CardPost를 게시판(share 탭)에 공유한 레코드

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shared_cards",
        help_text="공유한 사용자",
    )
    cardpost = models.ForeignKey(
        "join.CardPost",                # join 앱에 이미 존재
        on_delete=models.CASCADE,
        related_name="shared_cards",
        help_text="원본 카드",
    )
    description = models.TextField(help_text="추가 설명")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "share_sharedcard"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.cardpost_id} by {self.user_id}"
