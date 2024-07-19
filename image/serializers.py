from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'image_file', 'gender', 'master_category',
                  'sub_category', 'article_type', 'base_colour', 'season',
                  'year', 'usage', 'product_display_name']


class ImageQuerySerializer(serializers.Serializer):
    query_image = serializers.ImageField()
    k = serializers.IntegerField(default=5, min_value=1, max_value=10)
