from rest_framework import generics, permissions, status
from rest_framework.response import Response
from join.models import CardPost
from join.serializers import CardPostSerializer
from join.utils import increase_rank_score # 랭킹

class CardPostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardPostSerializer

    def get_queryset(self):
        return CardPost.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        card = serializer.save(user=self.request.user)
        increase_rank_score(card.user)