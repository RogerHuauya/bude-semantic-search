from django.db import models
from pgvector.django import VectorField, HnswIndex


class Image(models.Model):
    title = models.CharField(max_length=100)
    image_file = models.FileField(upload_to='image_files/')
    embedding = VectorField(null=True, blank=True, dimensions=768)
    gender = models.CharField(max_length=50, null=True, blank=True)
    master_category = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)
    article_type = models.CharField(max_length=100, null=True, blank=True)
    base_colour = models.CharField(max_length=50, null=True, blank=True)
    season = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    usage = models.CharField(max_length=50, null=True, blank=True)
    product_display_name = models.CharField(max_length=255, null=True,
                                            blank=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            HnswIndex(
                name="image_embedding_index",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]
