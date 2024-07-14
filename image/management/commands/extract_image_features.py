import torch
from PIL import Image as PILImage
from transformers import AutoImageProcessor, AutoModel
from django.core.management.base import BaseCommand
from image.models import Image

# Load the pre-trained model and processor
model_ckpt = "harshp8l/Fashion-Product-Images"
processor = AutoImageProcessor.from_pretrained(model_ckpt)
model = AutoModel.from_pretrained(model_ckpt)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def extract_features(image_file):
    img = PILImage.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = processor(images=img, return_tensors="pt").to(device)
    with torch.no_grad():
        embeddings = model(**img).last_hidden_state[:,
                     0].cpu().numpy().flatten()
    return embeddings


class Command(BaseCommand):
    help = 'Extract features from image files and store them in the database'

    def handle(self, *args, **kwargs):
        for image in Image.objects.all():
            with image.image_file.open('rb') as image_file:
                embeddings = extract_features(image_file)
                image.embedding = embeddings
                image.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully extracted and saved embeddings for {image.title}'))
