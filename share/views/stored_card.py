from rest_framework import status, views, permissions
from rest_framework.response import Response
from share.models import SharedCard
from share.serializers.stored_card import StoredCardSerializer
from share.services.stored_card import StoredCardService

class StoredCardCreateDeleteView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = StoredCardSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        shared_card = serializer.validated_data["sharedcard"]

        stored = StoredCardService.add(user, shared_card)
        return Response(StoredCardSerializer(stored).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        shared_card_id = request.data.get("sharedcard")
        shared_card = SharedCard.objects.get(pk=shared_card_id)

        deleted = StoredCardService.remove(user, shared_card)
        return Response({"deleted": deleted}, status=status.HTTP_204_NO_CONTENT)
    