from rest_framework import exceptions, status
from django.db import IntegrityError, transaction
from share.models import StoredCard, SharedCard

class AlreadyStoredException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 이 공유카드를 보관했습니다."
    default_code = "already_stored"

class StoreDoesNotExistException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "보관하지 않은 공유카드는 보관 취소할 수 없습니다."
    default_code = "store_not_found"

class StoredCardService:
    @classmethod
    @transaction.atomic
    def add(cls, user, sharedcard) -> StoredCard:
        if sharedcard.user != user:
            raise exceptions.PermissionDenied("본인이 생성한 공유카드만 보관할 수 있습니다.")
        if StoredCard.objects.filter(sharedcard=sharedcard).exists():
            raise AlreadyStoredException()
        return StoredCard.objects.create(user=user, sharedcard=sharedcard)

    @classmethod
    @transaction.atomic
    def remove(cls, user, sharedcard) -> int:
        try:
            stored = StoredCard.objects.get(sharedcard=sharedcard)
            if stored.user != user:
                raise exceptions.PermissionDenied("본인이 저장한 공유카드만 보관 취소할 수 있습니다.")
            deleted, _ = stored.delete()
            return deleted
        except StoredCard.DoesNotExist:
            raise StoreDoesNotExistException()
