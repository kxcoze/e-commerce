from django.test import TestCase

from users.models import User
from products.models import Product

from .models import Order, Product_Order


class OrderTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="User 1")

    def test_check_user_has_orders(self):
        order1 = Order.objects.create(customer=self.user1)
        order2 = Order.objects.create(customer=self.user1)
        self.assertSequenceEqual(self.user1.orders.all(), [order1, order2])

    def test_create_order_with_products(self):
        PRODUCT_1_AMOUNT = 10
        PRODUCT_2_AMOUNT = 100
        product1 = Product.objects.create(
            name="Product 1", price=2000, amount=PRODUCT_1_AMOUNT
        )
        product2 = Product.objects.create(
            name="Product 2", price=10000, amount=PRODUCT_2_AMOUNT
        )
        order1 = Order.objects.create(customer=self.user1)

        po1 = Product_Order.objects.create(
            order=order1, product=product1, product_amount=PRODUCT_1_AMOUNT
        )
        self.assertSequenceEqual(order1.products.all(), [product1])
        self.assertSequenceEqual(product1.orders.all(), [order1])
        self.assertEqual(product1.amount, 0)
        po2 = Product_Order.objects.create(
            order=order1, product=product2, product_amount=PRODUCT_2_AMOUNT
        )
        self.assertSequenceEqual(product2.orders.all(), [order1])
        self.assertEqual(product2.amount, 0)

        self.assertSequenceEqual(order1.products.all(), [product1, product2])

    def test_create_order_with_grt_amount_than_allowed(self):
        ALLOWED_AMOUNT = 10
        RESTRICTED_AMOUNT = 1000000
        product1 = Product.objects.create(
            name="Product 1", price=2000, amount=ALLOWED_AMOUNT
        )
        order1 = Order.objects.create(customer=self.user1)

        po1 = Product_Order.objects.create(
            order=order1, product=product1, product_amount=ALLOWED_AMOUNT
        )
        self.assertEqual(po1.product_amount, ALLOWED_AMOUNT)

        po2 = Product_Order(
            order=order1, product=product1, product_amount=RESTRICTED_AMOUNT
        )
        self.assertGreater(RESTRICTED_AMOUNT, ALLOWED_AMOUNT)
        self.assertRaises(ValueError, lambda: po2.save())

    def test_check_order_price(self):
        PRODUCT_1_AMOUNT, PRODUCT_1_PRICE = 10, 5000
        PRODUCT_2_AMOUNT, PRODUCT_2_PRICE = 50, 10000
        product1 = Product.objects.create(
            name="Product 1", price=PRODUCT_1_PRICE, amount=PRODUCT_1_AMOUNT
        )
        product2 = Product.objects.create(
            name="Product 2", price=PRODUCT_2_PRICE, amount=PRODUCT_2_AMOUNT
        )

        order1 = Order.objects.create(customer=self.user1)
        po1 = Product_Order.objects.create(
            order=order1, product=product1, product_amount=PRODUCT_1_AMOUNT
        )
        self.assertEqual(order1.price, PRODUCT_1_AMOUNT * PRODUCT_1_PRICE)
        # Clear cached value of price
        del order1.price

        po2 = Product_Order.objects.create(
            order=order1, product=product2, product_amount=PRODUCT_2_AMOUNT
        )
        self.assertEqual(
            order1.price,
            PRODUCT_1_AMOUNT * PRODUCT_1_PRICE + PRODUCT_2_AMOUNT * PRODUCT_2_PRICE,
        )
