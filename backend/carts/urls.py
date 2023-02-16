from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('my/', views.CartView.as_view()),
]
