from rest_framework import serializers

from .models import Order
from products.serializers import ProductSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: Make ProductMiniSerializer for proper nested objects
    products = ProductSerializer(many=True)
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Order
        fields = ["id", "status", "products", "price"]

