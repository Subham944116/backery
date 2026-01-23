from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class ProductCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
    
        serializer = ProductSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        
        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(
                product=product,
                image=image
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        products = Product.objects.all().order_by('-created_at')

    
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
