from django.contrib import admin
from .models import (
    SharedCard,
    Comment,
    CardLike,
    CardReport,
    PinnedCard,
    StoredCard,
    UserMissionState,
    CardMission,
)

admin.site.register(SharedCard)
admin.site.register(Comment)
admin.site.register(CardLike)
admin.site.register(CardReport)
admin.site.register(PinnedCard)
admin.site.register(StoredCard)
admin.site.register(UserMissionState)
admin.site.register(CardMission)
