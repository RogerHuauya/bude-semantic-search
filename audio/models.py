from django.db import models
from pgvector.django import VectorField


class Audio(models.Model):
    track_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio_files/')
    embedding = VectorField(null=True, blank=True, dimensions=360)

    def __str__(self):
        return self.title
