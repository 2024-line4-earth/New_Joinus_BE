from django.urls import path, include
from rest_framework.routers import DefaultRouter

from share.views.shared_card import (
    SharedCardListCreateView,
    SharedCardDetailView,
)
from share.views.comment import CommentViewSet
from share.views.card_like import CardLikeCreateDeleteView
from share.views.card_report import CardReportCreateView
from share.views.pin import PinnedSharedCardCreateDeleteView

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("sharedcards/", SharedCardListCreateView.as_view(), name="sharedcard-list-and-create"),
    path("sharedcards/<int:pk>/", SharedCardDetailView.as_view(), name="sharedcard-detail"),
    path("likes/", CardLikeCreateDeleteView.as_view(), name="card-like"),
    path("reports/", CardReportCreateView.as_view(), name="card-report"),
    path("pins/", PinnedSharedCardCreateDeleteView.as_view(), name="pin"),
]
