from rest_framework import status, views, permissions
from rest_framework.response import Response
from share.models import CardLike
from share.serializers.card_like import CardLikeSerializer

class CardLikeCreateDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 좋아요 생성
    def post(self, request):
        serializer = CardLikeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        like = serializer.save()
        return Response(CardLikeSerializer(like).data, status=201)

    # 좋아요 취소
    def delete(self, request):
        user = request.user
        sharedcard_id = request.data.get("sharedcard")
        qs = CardLike.objects.filter(user=user, sharedcard_id=sharedcard_id)
        deleted, _ = qs.delete()
        return Response({"deleted": deleted}, status=status.HTTP_204_NO_CONTENT)
