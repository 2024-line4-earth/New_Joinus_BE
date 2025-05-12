from django.shortcuts import get_object_or_404
from rest_framework import status, views, permissions
from rest_framework.response import Response
from share.models import SharedCard
from share.serializers.shared_card import (
    SharedCardSerializer,
)
class SharedCardListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = SharedCard.objects.select_related("user", "cardpost").all()
        serializer = SharedCardSerializer(queryset, many=True, hide_large_image_url=True)
        return Response({"sharedcards": serializer.data})
    
    def post(self, request):
        serializer = SharedCardSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            shared_card = serializer.save()
            return Response(SharedCardSerializer(shared_card, context={"request": request}, hide_is_liked=False).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SharedCardDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        shared_card = get_object_or_404(SharedCard.objects.select_related("user", "cardpost"), pk=pk)
        serializer = SharedCardSerializer(shared_card, context={"request": request}, hide_is_liked=False)
        return Response(serializer.data)
    