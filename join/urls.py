from django.urls import path
from join.views import (
    CardPostApiView,
    CardPostDetailView,
    UserTutorialStateRetrieveUpdateView,
    AvailableFrameApiView,
)

urlpatterns = [
    path("cards/", CardPostApiView.as_view(), name="cardpost-api-view"),
    path("cards/<int:pk>/", CardPostDetailView.as_view(), name="cardpost-detail-view"),
    path("tutorial/", UserTutorialStateRetrieveUpdateView.as_view(), name="tutorial-state"),
    path("frames/", AvailableFrameApiView.as_view(), name="available-frame-list"),
]
