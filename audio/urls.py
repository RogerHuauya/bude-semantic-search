from django.urls import path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'audio', views.AudioModelViewSet)

urlpatterns = [
    path('knn-sequential-audio-search/',
         views.KNNSequentialAudioSearch.as_view(),
         name='knn-sequential-audio-search'),
    path('knn-rtree-audio-search/',
         views.KNNRTreeAudioSearch.as_view(),
         name='knn-rtree-audio-search'),
    path('knn-high-dim-audio-search/',
         views.KNNHighDimAudioSearch.as_view(),
         name='knn-high-dim-audio-search'),
]

urlpatterns += router.urls
