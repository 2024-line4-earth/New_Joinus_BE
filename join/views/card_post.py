from django.shortcuts import get_object_or_404
from rest_framework import views, generics, permissions, status
from rest_framework.response import Response
from join.models import CardPost
from join.serializers import CardPostSerializer
from join.utils import increase_rank_score # 랭킹
from join.services import TutorialStateService
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied

class CardPostApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        TutorialStateService.check_tutorial_state(user=request.user)

    def get(self, request):
        queryset = CardPost.objects.filter(user=request.user)
        serializer = CardPostSerializer(queryset, many=True, context={"request": request}, hide_large_image_url=True)
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
        serializer = CardPostSerializer(cardpost)
        return Response(serializer.data)
