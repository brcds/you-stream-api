from rest_framework import serializers

from app_category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    id = serializers.ReadOnlyField(read_only=True)
    title_category = serializers.CharField(
        required=True, error_messages={"blank": "informe titulo da categoria"}
    )
    color = serializers.CharField(
        required=True, error_messages={"blank": "informe a cor da categoria"}
    )
