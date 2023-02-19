from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User
from products.models import Product
from .views import SignupView, LoginView, LogoutView


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="User 1")

    def test_check_user_favorites(self):
        product1 = Product.objects.create(name="Product 1", amount=50, price=1000)
        product2 = Product.objects.create(name="Product 2", amount=50, price=1337)
        self.user1.favorites.add(product1)

        self.assertSequenceEqual(self.user1.favorites.all(), [product1])

        self.user1.favorites.add(product2)
        self.assertSequenceEqual(self.user1.favorites.all(), [product1, product2])

        searched_product = self.user1.favorites.filter(name="Product 1").first()
        self.assertEqual(searched_product, product1)


class UserViewTestCase(APITestCase):
    def test_signup_view(self):
        url = reverse("users-signup")
        email = "test@example.com"
        password = "test"
        data = {
            "email": email,
            "password1": password,
            "password2": password,
        }

        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, email)

    def test_login_view_with_post(self):
        url = reverse("users-login")
        email = "test@example.com"
        password = "test"
        data = {"email": email, "password": password}

        User.objects.create_user(email=email, password=password)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_user_login(self):
        email = "test@example.com"
        password = "test"

        User.objects.create_user(email=email, password=password)
        is_ok = self.client.login(email=email, password=password)

        self.assertTrue(is_ok)

    def test_user_logout(self):
        url = reverse("users-logout")
        email = "test@example.com"
        password = "test"

        User.objects.create_user(email=email, password=password)
        self.client.login(email=email, password=password)

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
