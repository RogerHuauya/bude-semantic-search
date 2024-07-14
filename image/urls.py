from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'image', views.ImageModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]