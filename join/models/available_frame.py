from django.db import models
from market.models import Purchase  # market 앱의 구매 이력

class AvailableFrame(models.Model):
    purchase   = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="frames")
    frame_name = models.CharField(max_length=100)

    class Meta:
        db_table = "available_frame"

    def __str__(self):
        return f"{self.frame_name}"
