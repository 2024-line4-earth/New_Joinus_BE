from rest_framework import serializers
from share.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ["id", "user", "sharedcard", "content", "created_at"]
        read_only_fields = ["created_at"]
