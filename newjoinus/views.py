from django.http import HttpResponse
from rest_framework import views
from django.db import connections
from django.db.utils import OperationalError

class HealthCheckView(views.APIView):

    def get(self, request):
        try:
            connections["default"].cursor()  # DB 커넥션 체크
        except OperationalError:
            return HttpResponse(status=503)

        # Redis, S3 체크 필요시 추가하기
        return HttpResponse("READY", content_type="text/plain")
    