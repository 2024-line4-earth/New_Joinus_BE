from django.db import models
from users.models import User

class Us(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# 데일리 메세지들
class DailyMessage(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:20]

# 지정된 데일리 메세지
class SelectedDailyMessage(models.Model):
    date = models.DateField(unique=True)
    message = models.ForeignKey(DailyMessage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}: {self.message.content[:20]}"