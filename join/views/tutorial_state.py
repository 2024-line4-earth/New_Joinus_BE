from rest_framework import generics, permissions
from join.models import UserTutorialState
from join.serializers import UserTutorialStateSerializer

class UserTutorialStateRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserTutorialStateSerializer

    def get_object(self):
        obj, _ = UserTutorialState.objects.get_or_create(user=self.request.user)
        return obj
    