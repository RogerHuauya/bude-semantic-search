import librosa
import numpy as np

from django.core.management.base import BaseCommand
from sklearn.preprocessing import StandardScaler

from audio.models import Audio


def extract_features(audio_object):
    scaler = StandardScaler()
    # Cargar el archivo de audio
    y, sr = librosa.load(audio_object)

    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    print(chroma_stft.shape)
    # Estandarizamos
    chroma_stft = scaler.fit_transform(chroma_stft.T)
    chroma_stft = chroma_stft.T
    # Dividir en segmentos uniformes
    num_segments = 30
    segment_len = chroma_stft.shape[1] // num_segments

    # Tomar la media de cada segmento
    chroma_stft_uniform = np.mean(
        chroma_stft[:, :num_segments * segment_len].reshape(12, -1,
                                                            segment_len),
        axis=2)
    # Concatenar todas las características en un solo vector
    features = chroma_stft_uniform.flatten()

    return features


class Command(BaseCommand):
    help = 'Extract features from audio files'

    def handle(self, *args, **kwargs):
        for audio in Audio.objects.all():
            features = extract_features(audio.audio_file)
            audio.embedding = features
            audio.save()