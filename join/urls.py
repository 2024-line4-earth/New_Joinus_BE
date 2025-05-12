from django.urls import path
from join.views import (
    CardPostListCreateView,
    UserTutorialStateRetrieveUpdateView,
    AvailableFrameApiView,
)

urlpatterns = [
    path("cards/", CardPostListCreateView.as_view(), name="cardpost-list-create"),
    path("tutorial/", UserTutorialStateRetrieveUpdateView.as_view(), name="tutorial-state"),
    path("frames/", AvailableFrameApiView.as_view(), name="available-frame-list"),
]
