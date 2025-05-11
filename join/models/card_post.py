from django.db import models
from django.conf import settings

class Keyword(models.TextChoices):
    DISPOSABLES = "DISPOSABLES", "일회용품"
    RECYCLING = "RECYCLING", "분리수거"
    TUMBLER = "TUMBLER", "텀블러"
    STANDBY_POWER = "STANDBY_POWER", "대기전력"
    OTHER = "OTHER", "기타"

class CardPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name="card_posts")
    image_key = models.CharField(max_length=150)
    keywords = models.JSONField()              # 문자열 배열
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "card_post"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"CardPost({self.id}) by {self.user_id} in {self.created_at}"
