from django.core.management.base import BaseCommand
from inverted_index.custom_inverted_index import InvertedIndex


class Command(BaseCommand):
    help = 'Build the inverted index and store the files in the database'

    def handle(self, *args, **kwargs):
        InvertedIndex("spotify_songs.csv", "lyrics", 4000)
        self.stdout.write(self.style.SUCCESS(
            'Successfully built the inverted index and stored files'))
