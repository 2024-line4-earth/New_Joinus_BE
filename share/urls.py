from django.urls import path, include
from rest_framework.routers import DefaultRouter

from share.views.shared_card import SharedCardViewSet
from share.views.comment import CommentViewSet
from share.views.card_like import CardLikeCreateDeleteView
from share.views.card_report import CardReportCreateView

router = DefaultRouter()
router.register(r"sharedcards", SharedCardViewSet, basename="sharedcard")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("likes/", CardLikeCreateDeleteView.as_view(), name="card-like"),
    path("reports/", CardReportCreateView.as_view(), name="card-report"),
]
