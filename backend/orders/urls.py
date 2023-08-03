from django.urls import path

from .views import OrderCartView, OrderView

urlpatterns = [
    path('my/', OrderView.as_view(), name="orders-my"),
    path("checkout/", OrderCartView.as_view(), name="orders-checkout"),
]

