from rest_framework import exceptions, status
from django.db import IntegrityError, transaction
from django.db.models import Sum
from share.models import (
    CardLike,
    SharedCard,
)

class AlreadyLikedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "이미 이 공유카드에 좋아요를 눌렀습니다."
    default_code = "already_liked"

class LikeDoesNotExistException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "좋아요를 누른 적이 없어 취소가 불가능합니다."
    default_code = "like_not_found"

class CardLikeService:
    @classmethod
    @transaction.atomic
    def add(cls, user, sharedcard) -> CardLike:
        sharedcard_locked = SharedCard.objects.select_for_update().get(pk=sharedcard.pk)
        like_count = sharedcard_locked.like_count + 1
        sharedcard_locked.like_count = like_count
        if CardLike.objects.filter(user=user, sharedcard=sharedcard).exists():
            raise AlreadyLikedException()
        card_like = CardLike.objects.create(user=user, sharedcard=sharedcard)
        sharedcard_locked.save(update_fields=["like_count"])
        return card_like

    @classmethod
    @transaction.atomic
    def remove(cls, user, sharedcard) -> int:
        sharedcard_locked = SharedCard.objects.select_for_update().get(pk=sharedcard.pk)
        like_count = sharedcard_locked.like_count
        try:
            like_count -= 1
            sharedcard_locked.like_count = like_count
            card_like = CardLike.objects.get(user=user, sharedcard=sharedcard)
            deleted, _ = card_like.delete()
            sharedcard_locked.save(update_fields=["like_count"])
            return deleted
        except CardLike.DoesNotExist:
            raise LikeDoesNotExistException()
        