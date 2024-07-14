from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ImageQuerySerializer(serializers.Serializer):
    query_image = serializers.ImageField()