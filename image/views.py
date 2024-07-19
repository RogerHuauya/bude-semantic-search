import torch
from time import time
from PIL import Image as PILImage
from transformers import AutoImageProcessor, AutoModel
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from pgvector.django import CosineDistance

from .models import Image
from .serializers import ImageSerializer, ImageQuerySerializer
from .custom_rtree import XRtree

model_ckpt = "harshp8l/Fashion-Product-Images"
processor = AutoImageProcessor.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

bude_tree = XRtree()


def extract_features(image_file):
    img = PILImage.open(image_file)
    img = processor(images=img, return_tensors="pt").to(device)
    with torch.no_grad():
        embeddings = model(**img).last_hidden_state[:,
                     0].cpu().numpy().flatten()
    return embeddings


class ImageModelViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ImageAPIView(APIView):
    serializer_class = ImageQuerySerializer

    def post(self, request):
        serializer = ImageQuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        query_image = serializer.validated_data['query_image']
        k = serializer.validated_data['k']
        query_embedding = extract_features(query_image)

        query_embedding = query_embedding.tolist()
        similar_images = Image.objects.annotate(
            distance=CosineDistance("embedding", query_embedding)
        ).order_by("distance")[:k]

        response_serializer = ImageSerializer(similar_images, many=True)
        response = {
            "status": "success",
            "data": response_serializer.data,
            "execution_time": 0.0
        }
        return Response(response,
                        status=status.HTTP_200_OK)


class RtreeAPIView(APIView):
    serializer_class = ImageQuerySerializer

    def post(self, request):
        serializer = ImageQuerySerializer(data=request.data)
        if bude_tree.is_empty():
            images = Image.objects.all().exclude(embedding=None)
            bude_tree.batch_insert(images)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        query_image = serializer.validated_data['query_image']
        k = serializer.validated_data['k']
        query_embedding = extract_features(query_image)
        t = time()
        similar_ids = bude_tree.top_k_nearest(query_embedding, k)
        execution_time = time() - t
        similar_images = Image.objects.filter(id__in=similar_ids)
        response_serializer = ImageSerializer(similar_images, many=True)
        response = {
            "status": "success",
            "data": response_serializer.data,
            "execution_time": execution_time
        }

        return Response(response, status=status.HTTP_200_OK)


class SequentialAPIView(APIView):
    serializer_class = ImageQuerySerializer

    def post(self, request):
        serializer = ImageQuerySerializer(data=request.data)
        if bude_tree.is_empty():
            images = Image.objects.all().exclude(embedding=None)
            bude_tree.batch_insert(images)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        query_image = serializer.validated_data['query_image']
        k = serializer.validated_data['k']
        query_embedding = extract_features(query_image)
        t = time()
        similar_ids = bude_tree.top_k_nearest_sequential(query_embedding, k)
        execution_time = time() - t
        similar_images = Image.objects.filter(id__in=similar_ids)
        response_serializer = ImageSerializer(similar_images, many=True)
        response = {
            "status": "success",
            "data": response_serializer.data,
            "execution_time": execution_time
        }
        return Response(response, status=status.HTTP_200_OK)
