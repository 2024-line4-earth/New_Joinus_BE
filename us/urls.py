from django.urls import path
from .views import *

urlpatterns = [
    path('main/', UsAPIView.as_view()),
]
