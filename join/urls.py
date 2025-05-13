from django.urls import path
from join.views import (
    CardPostApiView,
    CardPostDetailView,
    NotifyImageUrlShareView,
    UserTutorialStateRetrieveUpdateView,
    AvailableFrameApiView,
)

urlpatterns = [
    path("cards/", CardPostApiView.as_view(), name="cardpost-api-view"),
    path("cards/<int:pk>/", CardPostDetailView.as_view(), name="cardpost-detail-view"),
    path("cards/<int:pk>/notify/", NotifyImageUrlShareView.as_view(), name="cardpost-notify"),
    path("tutorial/", UserTutorialStateRetrieveUpdateView.as_view(), name="tutorial-state"),
    path("frames/", AvailableFrameApiView.as_view(), name="available-frame-list"),
]
