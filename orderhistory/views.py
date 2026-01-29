from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.models import CakeOrder
from .serializers import OrderHistorySerializer


# Create your views here.
class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = CakeOrder.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = OrderHistorySerializer(
            orders,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)
