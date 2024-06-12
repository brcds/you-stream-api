from rest_framework import serializers

from app_category.models import Category
from app_video.models import Video
from app_category.api.serializers import CategorySerializer


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        error_messages={
            "does_not_exist": "Categoria informada não existe."
        }
    )

    class Meta:
        model = Video
        fields = "__all__"

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        max_length=255, required=True, error_messages={"blank": "Informe um titulo"}
    )
    description = serializers.CharField(
        required=True, error_messages={"blank": "Informe uma descrição"}
    )
    url = serializers.URLField(required=True, error_messages={"blank": "Informe a URL"})

    def validate(self, data):
        if not data.get("category"):
            try:
                data["category"] = Category.objects.get(id=1)
            except Category.DoesNotExist:
                raise serializers.ValidationError(detail="Categoria padrão não existe.")
        return data

    def create(self, validated_data):
        category_data = validated_data.pop("category", None)
        if category_data is None:
            category_data = Category.objects.get(id=1)
        video = Video.objects.create(**validated_data, category=category_data)
        return video

    def update(self, instance, validated_data):
        category_data = validated_data.pop("category", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if category_data:
            instance.category = category_data
        instance.save()
        return instance
