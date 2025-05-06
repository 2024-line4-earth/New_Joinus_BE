from django.db import models
from django.conf import settings

class PointRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name="point_records")
    amount = models.IntegerField()            # +적립 / -차감
    balance = models.IntegerField()
    type = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table  = "point_record"
        ordering  = ["-created_at"]
