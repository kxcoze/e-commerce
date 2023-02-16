from django.test import TestCase

from products.models import Product
from users.models import User
from .models import Cart, CartItem
from .serializers import CartSerializer


class CartTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='User 1')
    
    def test_check_user_cart(self):
        # Check user's cart is not existing 
        self.assertRaises(Cart.DoesNotExist, lambda: Cart.objects.get(user=self.user1))
        
        # If a user has the cart, it should be empty 
        cart = Cart.objects.create(user=self.user1)
        cart_items = CartItem.objects.filter(cart=cart)
        self.assertSequenceEqual(cart_items, [])

        # Create and add product to the user's cart
        product1 = Product.objects.create(
            name='Product 1', amount=5, price=1000)
        cart_item1 = CartItem(product=product1, amount=100, cart=cart)
        cart_item1.save()

        # Check if the cart item is putted into cart
        cart_items = CartItem.objects.filter(cart=cart)
        # self.assertSequenceEqual(cart.products.all(), [cart_item1.product])
        self.assertSequenceEqual(cart_items, [cart_item1])

        # Find specific cart item
        specific_cart_item = CartItem.objects.filter(cart=cart, product=product1).first()
        self.assertEqual(specific_cart_item.product, product1)
        
        # Delete specific cart item from the cart
        specific_cart_item.delete()
        cart_items = CartItem.objects.filter(cart=cart)
        # self.assertSequenceEqual(cart.products.all(), [])
        self.assertSequenceEqual(cart_items, [])
    
    
    
class CartSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='User 1')   
    
    def test_cart_serializer_creating(self):
        cart = Cart.objects.create(user=self.user1)
        product1 = Product.objects.create(name='Product 1', price=5000, amount=10)
        product2 = Product.objects.create(name='Product 2', price=100, amount=200)
        cart_item1 = CartItem(product=product1, cart=cart, amount=10)
        cart_item1.save()
        cart_item2 = CartItem(product=product2, cart=cart, amount=15)
        cart_item2.save()
        serializer = CartSerializer(cart)