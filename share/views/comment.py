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

class CommentDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response({"detail": "해당 댓글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"detail": "해당 댓글을 삭제할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"detail": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
