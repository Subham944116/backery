from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *


# Create your views here.
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only addresses of logged-in user
        """
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Attach user automatically while creating address
        """
        serializer.save(user=self.request.user)


    @action(detail=False, methods=['post'], url_path='set-default')
    def set_default_address(self, request):
        serializer = SetDefaultAddressSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Default address updated successfully"},
            status=status.HTTP_200_OK
        )

