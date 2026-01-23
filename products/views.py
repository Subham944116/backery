from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status



class ProductCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data

        product = Product.objects.create(
            name=data.get('name'),
            category=data.get('category'),
            flavour=data.get('flavour'),
            weight=data.get('weight'),
            price=data.get('price'),
            description=data.get('description'),
            diet_type=data.get('diet_type'),
            is_vegetarian=data.get('is_vegetarian', False)
        )

        images = request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(
                product=product,
                image=image
            )

        serializer = ProductSerializer(
            product,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        products = Product.objects.all().order_by('-created_at')

        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
