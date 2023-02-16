from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User
from .models import Cart, CartItem
from products.serializers import ProductSerializer
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField(source='amount')

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        
        
class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ['products']
        

class CartItemAddSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(source='amount')

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']
        extra_kwargs = {
            'product_id': {'required': True},
            'quantity': {'required': True},
        }
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = get_object_or_404(Product, id=validated_data['product_id'])
        
        if not product.amount:
            raise serializers.ValidationError(
                {'not available': 'the product is not available'}
            )
        cart_item = CartItem.objects.filter(
            cart=user.cart,
            product=product,
        ).first()
        if cart_item:
            cart_item.amount += validated_data['amount']
            cart_item.save()
            return cart_item

        cart_item = CartItem(
            cart=user.cart,
            product=product,
            amount=validated_data['amount'],
        )
        cart_item.save()
        # TODO: add handling for product reducing after adding to user's cart
        return cart_item
    
    
class CartItemDelSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    
    def delete(self):
        user = self.context['request'].user
        product = get_object_or_404(Product, id=self.validated_data['product_id'])
        cart_items = CartItem.objects.filter(
            cart=user.cart,
            product=product,
        ).all()
        for item in cart_items:
            item.delete()