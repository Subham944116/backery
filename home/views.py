from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import *
from .serializers import *


# Create your views here.
class HomePageAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        hero = HomeHero.objects.filter(is_active=True).first()
        categories = HomeCategory.objects.filter(is_active=True)
        products = Product.objects.filter(is_featured=True)

        data = {
            "hero": HomeHeroSerializer(hero, context={'request': request}).data if hero else None,
            "categories": HomeCategorySerializer(categories, many=True, context={'request': request}).data,
            "featured_products": HomeProductSerializer(products, many=True, context={'request': request}).data,
        }

        return Response(data)
