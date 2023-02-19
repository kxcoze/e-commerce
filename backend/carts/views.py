from rest_framework import views, status
from rest_framework import authentication, permissions
from rest_framework.response import Response

from products.serializers import ProductSerializer
from .serializers import CartSerializer, CartItemAddSerializer, CartItemDelSerializer
from .decorators import check_cart_existing


class CartView(views.APIView):
    @check_cart_existing
    def get(self, request, format=None):
        if request.user.is_authenticated:
            serializer = CartSerializer(request.user.cart)
            return Response(serializer.data)
        # TODO: Handle anonymous user's cart
        return Response("Sorry there is no cart")

    @check_cart_existing
    def put(self, request, format=None):
        if request.user.is_authenticated:
            serializer = CartItemAddSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )
        # TODO: Handle anonymous user's cart
        return Response("You have no rights here, sorry")

    @check_cart_existing
    def delete(self, request, format=None):
        if request.user.is_authenticated:
            serializer = CartItemDelSerializer(
                data=request.data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )
        # TODO: Handle anonymous user's cart
        return Response("You have no rights here, sorry")
