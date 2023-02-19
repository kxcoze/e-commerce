from rest_framework import viewsets
from rest_framework import permissions

from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
