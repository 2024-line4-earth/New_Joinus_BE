from rest_framework import generics, permissions
from join.models import AvailableFrame
from join.serializers import AvailableFrameSerializer
from rest_framework.response import Response

class AvailableFrameListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = AvailableFrameSerializer

    def get_queryset(self):
        return AvailableFrame.objects.filter(purchase__user=self.request.user)
