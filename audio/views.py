from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .models import Audio
from .serializers import AudioSerializer


class KNNSequentialAudioSearch(APIView):
    def post(self, request):
        k = int(request.data.get('k', 10))
        audio_file = request.data.get('audio_file', None)

        if not audio_file:
            return Response({"error": "Audio file is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # process audio file
        # return k most similar audio files
        return Response({"message": "Audio file received"},
                        status=status.HTTP_200_OK)


class KNNRTreeAudioSearch(APIView):
    def post(self, request):
        k = int(request.data.get('k', 10))
        audio_file = request.data.get('audio_file', None)

        if not audio_file:
            return Response({"error": "Audio file is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # process audio file
        # return k most similar audio files
        return Response({"message": "Audio file received"},
                        status=status.HTTP_200_OK)


class KNNHighDimAudioSearch(APIView):
    def post(self, request):
        k = int(request.data.get('k', 10))
        audio_file = request.data.get('audio_file', None)

        if not audio_file:
            return Response({"error": "Audio file is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        # process audio file
        # return k most similar audio files
        return Response({"message": "Audio file received"},
                        status=status.HTTP_200_OK)


class AudioModelViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
