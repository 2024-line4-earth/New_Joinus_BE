from django.db import transaction
from django.db.models import Sum
from join.models import PointRecord

class PointService:
    @classmethod
    @transaction.atomic
    def add(cls, user, amount: int, msg: str) -> PointRecord:
        bal = cls.get_balance(user) + amount
        if bal < 0:
            raise ValueError("포인트 부족")
        return PointRecord.objects.create(user=user, amount=amount, balance=bal, type=msg)

    @staticmethod
    def get_balance(user) -> int:
        agg = PointRecord.objects.filter(user=user).aggregate(total=Sum("amount"))
        return agg["total"] or 0
