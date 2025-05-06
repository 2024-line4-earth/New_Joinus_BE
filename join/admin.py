from django.contrib import admin
from .models import (
    CardPost, UserTutorialState, AvailableFrame, PointRecord
)

admin.site.register(CardPost)
admin.site.register(UserTutorialState)
admin.site.register(AvailableFrame)
admin.site.register(PointRecord)
