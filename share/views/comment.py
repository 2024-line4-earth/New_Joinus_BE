from rest_framework import views, status, permissions
from rest_framework.response import Response
from share.models import Comment
from share.serializers.comment import CommentSerializer

class CommentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        sharedcard_id = request.query_params.get("sharedcard")
        if not sharedcard_id:
            return Response({"detail": "sharedcard 쿼리 파라미터가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Comment.objects.filter(sharedcard_id=sharedcard_id).select_related("user", "sharedcard")
        serializer = CommentSerializer(queryset, many=True, context={"request": request}, hide_commenter_info=False)
        return Response({"comments": serializer.data})

    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
