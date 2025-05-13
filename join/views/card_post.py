from django.shortcuts import get_object_or_404
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from constants import ServiceConfigConstants as SCC
from join.models import CardPost
from join.serializers import CardPostSerializer
from join.services import PointService
from join.utils import increase_rank_score # 랭킹
from join.services import TutorialStateService
from django.utils.timezone import now
from django.db.models import BooleanField, ExpressionWrapper, Q
from rest_framework.exceptions import PermissionDenied
from django.db import transaction

class CardPostApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        TutorialStateService.check_tutorial_state(user=request.user)
    
    def get(self, request):
        user = request.user
        query_params = request.query_params

        keyword_list = query_params.getlist("keywords")
        month = query_params.get("month")
        only_not_shared = query_params.get("only_not_shared", "false").lower() == "true"
        ordered_by_is_shared = query_params.get("ordered_by_is_shared", "false").lower() == "true"

        # 기본 쿼리셋: 로그인한 사용자의 카드만 조회
        queryset = CardPost.objects.filter(user=user)

        # 키워드 필터링 (OR 조건)
        if keyword_list:
            queryset = queryset.filter(keyword__in=keyword_list)

        # 월 필터링
        today = now()
        if month is None:
            month = today.month
        queryset = queryset.filter(created_at__year=today.year, created_at__month=int(month))

        # 공유 여부 필터링
        if only_not_shared:
            queryset = queryset.filter(shared_card__isnull=True)

        # 정렬 (기본 최신순)
        if ordered_by_is_shared:
            queryset = queryset.annotate(
                is_shared=ExpressionWrapper(
                    Q(shared_card__isnull=False),
                    output_field=BooleanField()
                )
            )
            queryset = queryset.order_by("is_shared","-created_at")
        else:    
            queryset = queryset.order_by("-created_at")

        serializer = CardPostSerializer(
            queryset,
            many=True,
            context={"request": request},
            hide_large_image_url=True,
        )

        return Response({"cardposts": serializer.data})

    def post(self, request):
        serializer = CardPostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            card = serializer.save(user=request.user)
            increase_rank_score(card.user)
            return Response(CardPostSerializer(card, context={"request": request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CardPostDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        cardpost = get_object_or_404(CardPost.objects.select_related("user"), pk=pk)
        if request.user != cardpost.user:
            raise PermissionDenied("자신이 작성한 실천카드만 조회할 수 있습니다.")
        serializer = CardPostSerializer(cardpost, hide_has_image_url_share_been_notified=False)
        return Response(serializer.data)

class NotifyImageUrlShareView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        user = request.user

        with transaction.atomic():
            cardpost = (
                CardPost.objects.select_for_update()
                .select_related("user")
                .get(pk=pk)
            )
            if user != cardpost.user:
                raise PermissionDenied("자신이 작성한 실천카드만 공유할 수 있습니다.")

            if cardpost.has_image_url_share_been_notified:
                return Response({"detail": "이미 공유된 이미지입니다."}, status=status.HTTP_202_ACCEPTED)

            cardpost.has_image_url_share_been_notified = True
            cardpost.save(update_fields=["has_image_url_share_been_notified"])

            PointService.add(user, SCC.CARDPOST_SHARE_NOTIFIED_POINT, "실천카드 이미지 링크 공유")

        return Response({"detail": "이미지 링크 공유에 대한 포인트가 정상적으로 지급되었습니다."}, status=status.HTTP_200_OK)
