from rest_framework import generics, permissions
from share.models import CardReport
from share.serializers.card_report import CardReportSerializer

class CardReportCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardReportSerializer
    queryset = CardReport.objects.all()
