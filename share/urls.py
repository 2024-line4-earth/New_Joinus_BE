from django.urls import path, include
from rest_framework.routers import DefaultRouter

from share.views.shared_card import (
    SharedCardView,
    SharedCardDetailView,
    MySharedCardView,
)
from share.views.comment import CommentViewSet
from share.views.card_like import CardLikeCreateDeleteView
from share.views.card_report import CardReportCreateView
from share.views.pin import PinnedSharedCardCreateDeleteView
from share.views.stored_card import StoredCardCreateDeleteView
from share.views.mission import MissionStateView

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("sharedcards/", SharedCardView.as_view(), name="sharedcard-list-and-create"),
    path("sharedcards/<int:pk>/", SharedCardDetailView.as_view(), name="sharedcard-detail"),
    path("sharedcards/my/", MySharedCardView.as_view(), name="my-sharedcard"),
    path("likes/", CardLikeCreateDeleteView.as_view(), name="card-like"),
    path("reports/", CardReportCreateView.as_view(), name="card-report"),
    path("pins/", PinnedSharedCardCreateDeleteView.as_view(), name="pin"),
    path("store/", StoredCardCreateDeleteView.as_view(), name="store"),
    path("mission/", MissionStateView.as_view(), name="mission"),
]
