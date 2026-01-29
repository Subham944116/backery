from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Count
import random

from .models import HomeHero, HomeCategory, Product
from .serializers import *
    

class HomePageAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        hero = HomeHero.objects.filter(is_active=True).first()
        categories = HomeCategory.objects.filter(is_active=True)

        # 🎯 RANDOM 4 PRODUCTS EVERY REFRESH
        product_ids = list(Product.objects.values_list('id', flat=True))
        random.shuffle(product_ids)
        random_products = Product.objects.filter(id__in=product_ids[:4])

        data = {
            "hero": HomeHeroSerializer(
                hero, context={'request': request}
            ).data if hero else None,

            "categories": HomeCategorySerializer(
                categories, many=True, context={'request': request}
            ).data,

            "featured_products": HomeProductSerializer(
                random_products, many=True, context={'request': request}
            ).data
        }

        return Response(data)
