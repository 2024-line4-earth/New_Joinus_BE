from rest_framework import status, views, permissions
from rest_framework.response import Response
from share.models import CardLike
from share.models import SharedCard
from share.serializers.card_like import CardLikeSerializer
from share.services import CardLikeService

class CardLikeCreateDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 좋아요 생성
    def post(self, request):
        serializer = CardLikeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        sharedcard = serializer.validated_data["sharedcard"]
        
        like = CardLikeService.add(user, sharedcard)
        return Response(CardLikeSerializer(like).data, status=status.HTTP_201_CREATED)

    # 좋아요 취소
    def delete(self, request):
        user = request.user
        sharedcard_id = request.data.get("sharedcard")
        sharedcard = SharedCard.objects.get(pk=sharedcard_id)

        deleted = CardLikeService.remove(user, sharedcard)
        return Response({"deleted": deleted}, status=status.HTTP_204_NO_CONTENT)
