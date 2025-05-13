from django.shortcuts import get_object_or_404
from rest_framework import status, views, permissions
from rest_framework.response import Response
from django.utils.timezone import now
from share.models import (
    SharedCard,
)
from share.serializers.shared_card import (
    SharedCardSerializer,
)
class SharedCardView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        query_params = request.query_params

        only_this_month = query_params.get("only_this_month", "false").lower() == "true"
        order = query_params.get("order", "recent")

        queryset = SharedCard.objects.select_related("cardpost")

        if only_this_month:
            today = now()
            queryset = queryset.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )

        if order == "likes":
            queryset = queryset.order_by("-like_count", "-created_at")
        else:
            queryset = queryset.order_by("-created_at")

        serializer = SharedCardSerializer(
            queryset,
            many=True,
            context={"request": request},
            hide_large_image_url=True,
            hide_is_liked=True,
            hide_is_pinned=True,
        )
        return Response({"sharedcards": serializer.data})


    def post(self, request):
        serializer = SharedCardSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            shared_card = serializer.save()
            return Response(SharedCardSerializer(shared_card, context={"request": request}, hide_is_liked=False, hide_is_pinned=False).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SharedCardDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        shared_card = get_object_or_404(SharedCard.objects.select_related("user", "cardpost"), pk=pk)
        serializer = SharedCardSerializer(shared_card, context={"request": request}, hide_is_liked=False, hide_is_pinned=False)
        return Response(serializer.data)
    
class MySharedCardView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        query_params = request.query_params

        are_targets_stored = query_params.get("are_targets_stored", "false").lower() == "true"

        queryset = SharedCard.objects.filter(user=user).select_related("cardpost")

        if are_targets_stored:
            queryset = queryset.filter(stored_by__user=user)
            queryset = queryset.order_by("-created_at")
        else:
            queryset = queryset.order_by("-pinned_by__user", "-created_at")

        serializer = SharedCardSerializer(
            queryset,
            many=True,
            context={"request": request},
            hide_large_image_url=True,
            hide_is_liked=True,
            hide_is_pinned=False,
            hide_is_stored=False,
        )
        return Response({"sharedcards": serializer.data})
