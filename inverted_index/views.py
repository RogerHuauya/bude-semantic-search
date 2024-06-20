from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Song


class PostgresSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        k = int(request.GET.get('k', 10))

        if not query:
            return Response({"error": "Query parameter is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        search_query = SearchQuery(query)
        songs = Song.objects.annotate(
            rank=SearchRank('search_vector', search_query)
        ).order_by('-rank')[:k]

        results = [
            {
                "track_id": song.track_id,
                "track_name": song.track_name,
                "track_artist": song.track_artist,
                "lyrics": song.lyrics,
                "rank": song.rank,
            }
            for song in songs
        ]

        return Response(results, status=status.HTTP_200_OK)


class CustomSearchAPIView(APIView):

    def get(self, request):
        query = request.GET.get('query', '')
        k = int(request.GET.get('k', 10))

        if not query:
            return Response({"error": "Query parameter is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        search_query = SearchQuery(query)
        songs = Song.objects.annotate(
            rank=SearchRank('search_vector', search_query)
        ).order_by('-rank')[:k]

        results = [
            {
                "track_id": song.track_id,
                "track_name": song.track_name,
                "track_artist": song.track_artist,
                "lyrics": song.lyrics,
                "rank": song.rank,
            }
            for song in songs
        ]
        return Response(results, status=status.HTTP_200_OK)
