import csv
from django.core.management.base import BaseCommand
from inverted_index.models import Song


class Command(BaseCommand):
    help = 'Load songs from a CSV file into the database'

    def handle(self, *args, **kwargs):
        csv_file = 'spotify_songs.csv'

        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                song, created = Song.objects.update_or_create(
                    track_id=row['track_id'],
                    defaults={
                        'track_name': row['track_name'],
                        'track_artist': row['track_artist'],
                        'lyrics': row['lyrics']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Successfully created song: {song.track_name}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Successfully updated song: {song.track_name}"))
        self.stdout.write(self.style.SUCCESS('Successfully loaded songs from CSV'))
