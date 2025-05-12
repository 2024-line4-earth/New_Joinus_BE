from rest_framework import exceptions, status
from django.db import IntegrityError, transaction
from share.models import PinnedSharedCard, SharedCard

class AlreadyPinnedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 이 공유카드를 고정했습니다."
    default_code = "already_pinned"

class PinDoesNotExistException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "고정하지 않은 공유카드는 고정 해제할 수 없습니다."
    default_code = "pin_not_found"

class PinnedSharedCardService:
    @classmethod
    @transaction.atomic
    def add(cls, user, shared_card) -> PinnedSharedCard:
        if PinnedSharedCard.objects.filter(user=user, shared_card=shared_card).exists():
            raise AlreadyPinnedException()
        return PinnedSharedCard.objects.create(user=user, shared_card=shared_card)

    @classmethod
    @transaction.atomic
    def remove(cls, user, shared_card) -> int:
        try:
            pin = PinnedSharedCard.objects.get(user=user, shared_card=shared_card)
            deleted, _ = pin.delete()
            return deleted
        except PinnedSharedCard.DoesNotExist:
            raise PinDoesNotExistException()
