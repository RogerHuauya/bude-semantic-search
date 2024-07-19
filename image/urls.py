from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'image', views.ImageModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pgvector/search/', views.ImageAPIView.as_view(),
         name='image-search'),
    path('rtree/search/', views.RtreeAPIView.as_view(), name='rtree-search'),
    path('sequential/search/', views.SequentialAPIView.as_view(),
         name='sequential-search'),
]
