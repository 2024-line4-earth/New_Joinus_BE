from rest_framework import exceptions
from rest_framework import status

from join.models import UserTutorialState

class TutorialNotCompletedError(exceptions.APIException):
    status_code = status.HTTP_202_ACCEPTED # 프론트 편의를 위해 202 설정
    default_detail = "튜토리얼을 완료해야 이 작업을 수행할 수 있습니다."
    default_code = "tutorial_incomplete"


class TutorialStateService:
    @classmethod
    def check_tutorial_state(cls, user):
        obj, _ = UserTutorialState.objects.get_or_create(user=user)
        if not obj.tutorial_completed:
            raise TutorialNotCompletedError()
