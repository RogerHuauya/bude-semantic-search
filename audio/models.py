from django.db import models


class Audio(models.Model):
    track_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio_files/')

    def __str__(self):
        return self.title