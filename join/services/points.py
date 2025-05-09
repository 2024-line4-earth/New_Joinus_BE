from rest_framework import exceptions, status
from django.db import transaction
from django.db.models import Sum
from join.models import PointRecord
from users.models import User

class InsufficientPointError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "보유 포인트가 부족합니다."
    default_code = "insufficient_points"

class PointService:
    @classmethod
    @transaction.atomic
    def add(cls, user, amount: int, msg: str) -> PointRecord:
        user_locked = User.objects.select_for_update().get(pk=user.pk)
        bal = cls.get_balance(user_locked) + amount
        if bal < 0:
            raise InsufficientPointError()
        user_locked.points = bal
        user_locked.save(update_fields=["points"])
        return PointRecord.objects.create(user=user_locked, amount=amount, balance=bal, type=msg)

    @staticmethod
    def get_balance(user) -> int:
        agg = PointRecord.objects.filter(user=user).aggregate(total=Sum("amount"))
        return agg["total"] or 0
