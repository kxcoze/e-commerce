from django.urls import path, include
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r"", viewsets.ProductViewSet)

urlpatterns = [
    path("", include(router.urls)),
]