from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Song(models.Model):
    track_id = models.CharField(max_length=255, unique=True)
    track_name = models.CharField(max_length=255)
    track_artist = models.CharField(max_length=255)
    lyrics = models.TextField()
    search_vector = SearchVectorField(null=True)

    def __str__(self):
        return f"{self.track_name} by {self.track_artist}"

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]


class IndexFile(models.Model):
    block_number = models.IntegerField()
    height = models.IntegerField()
    file = models.FileField(upload_to='blocks/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Block {self.block_number}, Height {self.height}"
