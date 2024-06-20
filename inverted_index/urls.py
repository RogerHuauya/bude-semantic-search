from django.urls import path
from inverted_index.views import PostgresSearchAPIView, CustomSearchAPIView

urlpatterns = [
    path('postgres-search/', PostgresSearchAPIView.as_view(), name='postgres-search'),
    path('custom-search/', CustomSearchAPIView.as_view(), name='custom-search'),
]