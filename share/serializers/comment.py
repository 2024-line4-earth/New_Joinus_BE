from rest_framework import serializers
from share.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sharedcard = serializers.PrimaryKeyRelatedField(queryset=Comment._meta.get_field("sharedcard").remote_field.model.objects.all(), write_only=True)
    commenter_info = serializers.SerializerMethodField();
    
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "commenter_info", 
            "sharedcard", 
            "content", 
            "created_at"
        ]
        read_only_fields = ["created_at"]

    def __init__(self, *args, **kwargs):
        hide_commenter_info = kwargs.pop("hide_commenter_info", True)
        super().__init__(*args, **kwargs)
        if hide_commenter_info:
            self.fields.pop("commenter_info", None)

    def get_commenter_info(self, obj):
        user = obj.user
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            is_owner = user == request.user
        else:
            is_owner = False
        return {
            "user_id": user.id,
            "username": user.username,
            "is_owner": is_owner,
        }
