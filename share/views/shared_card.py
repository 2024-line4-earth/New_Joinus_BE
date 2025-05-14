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
from share.pagination import SharedCardCursorPagination
from rest_framework.exceptions import PermissionDenied

class SharedCardView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SharedCardCursorPagination

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

        # 페이징 처리
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = SharedCardSerializer(
            page,
            many=True,
            context={"request": request},
            hide_large_image_url=True,
            hide_is_liked=True,
            hide_is_pinned=True,
        )
        return paginator.get_paginated_response({"sharedcards": serializer.data})


    def post(self, request):
        serializer = SharedCardSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            shared_card = serializer.save()
            return Response(SharedCardSerializer(shared_card, context={"request": request}, hide_is_liked=False, hide_is_pinned=False).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SharedCardDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        sharedcard = get_object_or_404(SharedCard.objects.select_related("user", "cardpost"), pk=pk)
        if sharedcard.user != user:
            raise PermissionDenied("자신이 생성한 공유카드만 수정/삭제할 수 있습니다.")
        return sharedcard

    def get(self, request, pk):
        shared_card = get_object_or_404(SharedCard.objects.select_related("user", "cardpost"), pk=pk)
        serializer = SharedCardSerializer(shared_card, context={"request": request}, hide_is_liked=False, hide_is_pinned=False, hide_author_info=False)
        return Response(serializer.data)

    def put(self, request, pk):
        shared_card = self.get_object(pk, request.user)
        serializer = SharedCardSerializer(
            shared_card,
            data=request.data,
            partial=True,  # 부분 업데이트 허용
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        # description 필드만 업데이트 허용
        if set(serializer.validated_data.keys()) - {"description"}:
            return Response({"detail": "description 필드만 수정할 수 있습니다."}, status=400)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        sharedcard = self.get_object(pk, request.user)
        deleted, _ = sharedcard.delete()
        return Response({"deleted": deleted}, status=status.HTTP_204_NO_CONTENT)

class MySharedCardView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = SharedCardCursorPagination

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
    
        # 페이징 처리
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = SharedCardSerializer(
            page,
            many=True,
            context={"request": request},
            hide_large_image_url=True,
            hide_is_liked=True,
            hide_is_pinned=False,
            hide_is_stored=False,
        )
        return paginator.get_paginated_response({"sharedcards": serializer.data})
