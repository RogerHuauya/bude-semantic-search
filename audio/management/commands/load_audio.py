import os
import requests

from django.core.management.base import BaseCommand
from django.core.files import File
from audio.models import Audio
import audio.utils as utils
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Load audio files from a CSV file into the database'

    def handle(self, *args, **kwargs):
        AUDIO_DIR = os.environ.get('AUDIO_DIR', 'fma_small')
        csv_file = 'tracks.csv'

        if not os.path.exists(csv_file):
            print("Downloading CSV file")
            url = "https://storage.googleapis.com/rogers-bucket/tracks.csv"
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open(csv_file, 'wb') as f:
                for data in tqdm(response.iter_content(1024), total=total_size//1024, unit='KB'):
                    f.write(data)

        tracks = utils.load(csv_file)
        small_tracks = tracks[tracks['set', 'subset'] <= 'small'][:5]

        for track_id, track in small_tracks.iterrows():
            source_path = utils.get_audio_path(AUDIO_DIR, track_id)

            # Open the file and store it in the audio object
            with open(source_path, 'rb') as audio_file:
                audio = Audio(
                    track_id=track_id,
                    title=track['track', 'title'],
                    audio_file=File(audio_file, name=f'{track_id}.mp3')
                )
                audio.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully loaded and saved {track_id} - {track["track", "title"]}'))
