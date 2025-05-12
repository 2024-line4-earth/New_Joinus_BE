from rest_framework import views, permissions
from join.models import AvailableFrame
from join.serializers import AvailableFrameSerializer
from rest_framework.response import Response

class AvailableFrameApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = AvailableFrameSerializer

    def get(self, request):
        frames_qs = AvailableFrame.objects.filter(purchase__user=request.user)
        frame_names = list(frames_qs.values_list("frame_name", flat=True))
        return Response({"frame_names": frame_names})
