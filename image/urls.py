from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'image', views.ImageModelViewSet)
router.register(r'rtree', views.RtreeAPIView, basename='rtree')

urlpatterns = [
    path('', include(router.urls)),
]