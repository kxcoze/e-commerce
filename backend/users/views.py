from django.contrib.auth import login, logout
from rest_framework import views, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes

from .serializers import LoginSerializer, SignupSerializer
from .permissions import IsAnonymousUser

class SignupView(views.APIView):
    permission_classes = (IsAnonymousUser,)
    
    def post(self, request, format=None):
        serializer = SignupSerializer(data=self.request.data,
                                      context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_201_CREATED)

class LoginView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, 
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
    

class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request, format=None):
    return Response({
        'signup': reverse('users-signup', request=request, format=format),
        'login': reverse('users-login', request=request, format=format),
        'logout': reverse('users-logout', request=request, format=format),
    })