from rest_framework import serializers
from join.models import CardPost, Keyword
from join.services import S3Service, PointService
from join.utils import build_image_key
from constants import ServiceConfigConstants as SCC 

class CardPostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True)
    keywords = serializers.ListField(
        child=serializers.ChoiceField(choices=Keyword.choices),
        min_length=1,
        allow_empty=False,
        write_only=True,
    )
    small_image_url = serializers.SerializerMethodField(read_only=True)
    large_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CardPost
        fields = ["id", "keywords", "image",
                    "small_image_url", "large_image_url", "created_at"]
        read_only_fields = ["id", "small_image_url", "large_image_url","created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        img_file = validated_data.pop("image")
        keywords = validated_data.pop("keywords")

        key = build_image_key(user.id, ext=img_file.name.split(".")[-1])
        S3Service.upload_fileobj(img_file, key, content_type=img_file.content_type)

        instance = CardPost.objects.create(
            user=user,
            image_key=key,
            keywords=keywords,
        )
        PointService.add(user, SCC.CARDPOST_CREATE_POINT, "실천 카드 생성")
        return instance

    def get_small_image_url(self, obj):
        return S3Service.generate_small_image_presigned_get_url(obj.image_key)
    
    def get_large_image_url(self, obj):
        return S3Service.generate_large_image_presigned_get_url(obj.image_key)

