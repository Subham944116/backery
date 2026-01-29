from shop.models import Cart, CartItem
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status

from .models import CakeOrder
from .serializers import CakeOrderSerializer

# Create your views here.
class CakeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        serializer = CakeOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        flavors = [
            {"value": key, "label": label}
            for key, label in CakeOrder.FLAVOR_CHOICES
        ]

        shapes = [
            {"value": key, "label": label}
            for key, label in CakeOrder.SHAPE_CHOICES
        ]

        colors = [
            {"value": key, "label": label}
            for key, label in CakeOrder.COLOR_CHOICES
        ]

        weights = [
            {"value": weight, "price": price}
            for weight, price in CakeOrder.PRICE_MAP.items()
        ]

        return Response({
            "flavors": flavors,
            "shapes": shapes,
            "colors": colors,
            "weights": weights
        }, status=status.HTTP_200_OK)


class AddCustomCakeToCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cake = CakeOrder.objects.get(
            id=order_id,
            user=request.user
        )

        CartItem.objects.create(
            cart=cart,
            custom_cake=cake,
            quantity=1
        )

        return Response({"message": "Custom cake added to cart"})



 