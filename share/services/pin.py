from rest_framework import exceptions, status
from django.db import IntegrityError, transaction
from share.models import PinnedCard, SharedCard

class AlreadyPinnedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 이 공유카드를 고정했습니다."
    default_code = "already_pinned"

class PinDoesNotExistException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "고정하지 않은 공유카드는 고정 해제할 수 없습니다."
    default_code = "pin_not_found"

class PinnedCardService:
    @classmethod
    @transaction.atomic
    def add(cls, user, sharedcard) -> PinnedCard:
        if PinnedCard.objects.filter(user=user, sharedcard=sharedcard).exists():
            raise AlreadyPinnedException()
        return PinnedCard.objects.create(user=user, sharedcard=sharedcard)

    @classmethod
    @transaction.atomic
    def remove(cls, user, sharedcard) -> int:
        try:
            pin = PinnedCard.objects.get(user=user, sharedcard=sharedcard)
            deleted, _ = pin.delete()
            return deleted
        except PinnedCard.DoesNotExist:
            raise PinDoesNotExistException()
