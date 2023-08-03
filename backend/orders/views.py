from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Product_Order
from .serializers import OrderSerializer
from carts.serializers import CartSerializer
from carts.models import Cart, CartItem

class OrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        # View all orders of current user.
        user = request.user
        orders = Order.objects.filter(customer=user)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class OrderCartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        # Calculate all data for future order with current cart.
        user = request.user
        cart_items = CartItem.objects.filter(cart=user.cart)
        data = {}
        total = 0
        quantity = 0
        for item in cart_items:
            total += item.product.price * item.amount
            quantity += item.amount
        
        data["items"] = CartSerializer(user.cart).data
        data["total"] = total
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        # Performing request to create order according to current cart.
        user = request.user
        cart_items = CartItem.objects.filter(cart=user.cart)
        if not cart_items:
            # If user doesn't have anything in cart just return 400
            return Response(f'Your cart is empty, please go and add some products!', status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(customer=user)
        try:
            with transaction.atomic():
                for item in cart_items:
                    Product_Order.objects.create(order=order, product=item.product, product_amount=item.amount)
        except ValueError as e:
            order.delete()
            return Response(f'Some of your products in cart has invalid count!', status=status.HTTP_400_BAD_REQUEST)
        # Order is created, clearing all data in cart.
        cart_items.delete()
        return Response(f'Your order {order} was successfuly created!', status=status.HTTP_201_CREATED)
