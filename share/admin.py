from django.contrib import admin
from .models import (
    SharedCard,
    Comment,
    CardLike,
    CardReport,
)

admin.site.register(SharedCard)
admin.site.register(Comment)
admin.site.register(CardLike)
admin.site.register(CardReport)
