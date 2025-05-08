from rest_framework import viewsets, mixins, permissions

from share.models import SharedCard
from share.serializers.shared_card import (
    SharedCardSerializer,
)

class SharedCardViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SharedCard.objects.select_related("user", "cardpost")
    serializer_class = SharedCardSerializer

    def get_queryset(self):
        return self.queryset
