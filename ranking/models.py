from django.db import models
from users.models import User

class MonthlyCardStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    card_count = models.IntegerField()
    earliest_created_at = models.DateTimeField(null=True, blank=True) 
    rank = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'year', 'month')
        ordering = ['-card_count', 'earliest_created_at']

