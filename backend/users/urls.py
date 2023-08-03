from rest_framework import routers
from django.urls import path, include

from . import views, viewsets

router = routers.DefaultRouter()
router.register(r"list", viewsets.UserViewSet)

urlpatterns = [
    path("", views.api_root),
    path("signup/", views.SignupView.as_view(), name="users-signup"),
    path("login/", views.LoginView.as_view(), name="users-login"),
    path("logout/", views.LogoutView.as_view(), name="users-logout"),
    path("", include(router.urls))
]

urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]