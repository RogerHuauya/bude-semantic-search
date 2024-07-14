import torch
from PIL import Image as PILImage
from transformers import AutoImageProcessor, AutoModel
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from pgvector.django import CosineDistance

from .models import Image
from .serializers import ImageSerializer, ImageQuerySerializer

model_ckpt = "harshp8l/Fashion-Product-Images"
processor = AutoImageProcessor.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


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

    @action(detail=False, methods=['post'], url_path='search')
    def search(self, request):
        serializer = ImageQuerySerializer(data=request.data)
        if serializer.is_valid():
            query_image = serializer.validated_data['query_image']
            query_embedding = extract_features(query_image)

            query_embedding = query_embedding.tolist()
            similar_images = Image.objects.annotate(
                distance=CosineDistance("embedding", query_embedding)
            ).order_by("distance")[:5]

            response_serializer = ImageSerializer(similar_images, many=True)
            return Response(response_serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
