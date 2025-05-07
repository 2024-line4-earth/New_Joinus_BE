from rest_framework import viewsets, permissions, mixins
from share.models import Comment
from share.serializers.comment import CommentSerializer

class CommentViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.select_related("user", "sharedcard")
    serializer_class = CommentSerializer

    # /comments/?sharedcard=<id>
    def get_queryset(self):
        qs = self.queryset
        sc_id = self.request.query_params.get("sharedcard")
        if sc_id:
            qs = qs.filter(sharedcard_id=sc_id)
        return qs
