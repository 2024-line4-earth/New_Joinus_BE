import random
from rest_framework import views, permissions
from rest_framework.response import Response
from join.models import Keyword
from share.models import (
    UserMissionState,
    CardMission,
)

class MissionStateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        mission_state, _ = UserMissionState.objects.get_or_create(user=user)

        try:
            card_mission = mission_state.cardmission
        except CardMission.DoesNotExist:
            random_keyword = random.choice(Keyword.values)
            card_mission = CardMission.objects.create(
                mission_state=mission_state,
                keyword=random_keyword
            )

        return Response({
            "is_completed": mission_state.is_completed,
            "keyword": card_mission.keyword
        })
    