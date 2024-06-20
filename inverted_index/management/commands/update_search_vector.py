from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector

from inverted_index.models import Song


class Command(BaseCommand):
    help = 'Update search vector for songs'

    def handle(self, *args, **kwargs):
        Song.objects.update(search_vector=SearchVector('track_name', 'lyrics'))
        self.stdout.write(self.style.SUCCESS('Successfully updated search vectors'))
