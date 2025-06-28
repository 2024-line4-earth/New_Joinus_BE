from django.urls import path
from .views import *

urlpatterns = [
    path('main/', TopTwentyView.as_view()),
    path('sharelist/<int:user_id>/', RankUserSharedCardView.as_view()),
    path('notification/1/', NotificationOneView.as_view()),
    path('notification/2/', NotificationTwoView.as_view()),
    path('notification/3/', NotificationThreeView.as_view()),
]
