from django.core.management.base import BaseCommand
from image.models import Image


class Command(BaseCommand):
    help = 'Test command'

    def handle(self, *args, **kwargs):
        print("Hello, world!")

        queryset = Image.objects.all()[:5]
        var = []
        for img in queryset:
            var.append({"title": img.title, "vector": img.embedding, "id": img.id})
        print(var)


