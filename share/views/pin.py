from rest_framework import status, views, permissions
from rest_framework.response import Response
from share.models import SharedCard
from share.models import PinnedCard
from share.serializers.pin import PinnedSharedCardSerializer
from share.services.pin import PinnedCardService

class PinnedSharedCardCreateDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 핀 생성
    def post(self, request):
        serializer = PinnedSharedCardSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        shared_card = serializer.validated_data["sharedcard"]

        pinned = PinnedCardService.add(user, shared_card)
        return Response(PinnedSharedCardSerializer(pinned).data, status=status.HTTP_201_CREATED)

    # 핀 해제
    def delete(self, request):
        user = request.user
        shared_card_id = request.data.get("sharedcard")
        shared_card = SharedCard.objects.get(pk=shared_card_id)

        deleted = PinnedCardService.remove(user, shared_card)
        return Response({"deleted": deleted}, status=status.HTTP_204_NO_CONTENT)
