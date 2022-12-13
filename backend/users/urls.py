from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.api_root),
    path('login/', views.LoginView.as_view(), name='users-login'),
    path('logout/', views.LogoutView.as_view(), name='users-logout'),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]