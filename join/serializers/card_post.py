from rest_framework import serializers
from join.models import CardPost, Keyword
from join.services import S3Service, PointService
from join.utils import build_image_key
from constants import ServiceConfigConstants as SCC 

class CardPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    keyword = serializers.ChoiceField(
        choices=Keyword.choices,
    )
    small_image_url = serializers.SerializerMethodField(read_only=True)
    large_image_url = serializers.SerializerMethodField(read_only=True)
    is_shared = serializers.SerializerMethodField()
    has_image_url_share_been_notified = serializers.BooleanField(read_only=True)
    class Meta:
        model = CardPost
        fields = [
            "id", 
            "keyword",
            "image",
            "small_image_url", 
            "large_image_url", 
            "is_shared",
            "has_image_url_share_been_notified",
            "created_at"
        ]
        read_only_fields = ["id", "small_image_url", "large_image_url", "created_at"]

    def __init__(self, *args, **kwargs):
        hide_is_shared = kwargs.pop("hide_is_shared", False)
        hide_large_image_url = kwargs.pop("hide_large_image_url", False)
        hide_has_image_url_share_been_notified = kwargs.pop("hide_has_image_url_share_been_notified", True)
        super().__init__(*args, **kwargs)
        if hide_is_shared:
            self.fields.pop("is_shared", None)
        if hide_large_image_url:
            self.fields.pop("large_image_url", None)
        if hide_has_image_url_share_been_notified:
            self.fields.pop("has_image_url_share_been_notified", None)

    def create(self, validated_data):
        user = self.context["request"].user
        img_file = validated_data.pop("image")
        keyword = validated_data.pop("keyword")

        key = build_image_key(user.id, ext=img_file.name.split(".")[-1])
        S3Service.upload_fileobj(img_file, key, content_type=img_file.content_type)

        instance = CardPost.objects.create(
            user=user,
            image_key=key,
            keyword=keyword,
        )
        return instance

    def get_small_image_url(self, obj):
        return S3Service.generate_small_image_presigned_get_url(obj.image_key)
    
    def get_large_image_url(self, obj):
        return S3Service.generate_large_image_presigned_get_url(obj.image_key)

    def get_is_shared(self, obj):
        return hasattr(obj, "shared_card")
    