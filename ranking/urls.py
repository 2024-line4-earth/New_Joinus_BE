from django.urls import path
from .views import *

urlpatterns = [
    path('main/', TopTwentyView.as_view()),
    path('sharelist/<int:user_id>/', RankUserSharedCardView.as_view()),
]
