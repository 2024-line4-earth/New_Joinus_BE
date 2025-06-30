from rest_framework import views, permissions
from rest_framework.response import Response
from share.utils.mission import get_or_refresh_mission

class MissionStateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        mission_state, card_mission = get_or_refresh_mission(request.user)
        return Response({
            "is_completed": mission_state.is_completed,
            "keyword": card_mission.keyword
        })
