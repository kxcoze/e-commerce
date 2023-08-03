from rest_framework import views, status
from rest_framework.response import Response

from .serializers import CartSerializer, CartItemAddSerializer, CartItemDelSerializer


class CartView(views.APIView):
    # TODO: Add a Patch method for the view
    def get(self, request, format=None):
        if request.user.is_authenticated:
            serializer = CartSerializer(request.user.cart)
            return Response(serializer.data)
        # TODO: Handle anonymous user's cart
        return Response("Sorry there is no cart", status=status.HTTP_401_UNAUTHORIZED)

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
        return Response("You have no rights here, sorry", status=status.HTTP_401_UNAUTHORIZED)

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
        return Response("You have no rights here, sorry", status=status.HTTP_401_UNAUTHORIZED)
