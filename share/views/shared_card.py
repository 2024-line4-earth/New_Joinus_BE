from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from share.models import SharedCard
from share.serializers.shared_card import (
    SharedCardSerializer,
    SharedCardFinalizeSerializer,
)

class SharedCardViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SharedCard.objects.select_related("user", "cardpost")
    serializer_class = SharedCardSerializer

    # 필터링: /sharedcards/?is_finalized=true|false
    def get_queryset(self):
        qs = self.queryset
        flag = self.request.query_params.get("is_finalized")
        if flag in ("true", "false"):
            qs = qs.filter(is_finalized=(flag == "true"))
        return qs

    # is_finalized PATCH API
    @action(methods=["put"], detail=True)
    def finalize(self, request, pk=None):
        sc = self.get_object()
        serializer = SharedCardFinalizeSerializer(
            sc, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(SharedCardSerializer(sc).data)
