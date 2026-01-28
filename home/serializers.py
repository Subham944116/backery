from rest_framework import serializers
from .models import *


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)


class HomeProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'rating',
            'treat_type',
            'main_image'
        ]

    def get_main_image(self, obj):
        image = obj.images.filter(is_main=True).first()
        if image:
            request = self.context.get('request')
            return request.build_absolute_uri(image.image.url)
        return None


class HomeCategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = HomeCategory
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'icon'
        ]

    def get_icon(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.icon.url)


class HomeHeroSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()

    class Meta:
        model = HomeHero
        fields = [
            'badge_text',
            'title',
            'subtitle',
            'hero_image',
            'primary_button_text',
            'secondary_button_text'
        ]

    def get_hero_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.hero_image.url)

class HomePageSerializer(serializers.Serializer):
    hero = HomeHeroSerializer()
    categories = HomeCategorySerializer(many=True)
    featured_products = HomeProductSerializer(many=True)
