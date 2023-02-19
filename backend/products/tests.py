from django.test import TestCase

from .models import Product, Review
from users.models import User


class ProductTestCase(TestCase):
    def test_product_create(self):
        product1 = Product.objects.create(name="Product 1", price=5000, amount=50)
        self.assertEqual(product1.name, "Product 1")
        self.assertEqual(product1.price, 5000)
        self.assertEqual(product1.amount, 50)


class ReviewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="User 1")

    def test_create_review_for_product(self):
        product1 = Product.objects.create(name="Product 1", amount=100, price=10000)
        review = Review.objects.create(
            user=self.user1,
            product=product1,
            vote=3.5,
            comment="Nice one!",
        )
        self.assertSequenceEqual(Review.objects.filter(user=self.user1).all(), [review])
