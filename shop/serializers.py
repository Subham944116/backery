from custom_cake.serializers import CakeOrderSerializer
from rest_framework import serializers
from .models import Product, CartItem, Cart


# serializers.py
 

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        image = obj.images.filter(is_primary=True).first()

        if image and image.image and request:
            return request.build_absolute_uri(image.image.url)

        return None



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    custom_cake = CakeOrderSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'custom_cake',
            'image',
            'quantity',
            'total_price'
        ]

    def get_image(self, obj):
        request = self.context.get('request')

        if obj.product:
            image = obj.product.images.filter(is_primary=True).first()
            if image and image.image and request:
                return request.build_absolute_uri(image.image.url)

        if obj.custom_cake and obj.custom_cake.image and request:
            return request.build_absolute_uri(obj.custom_cake.image.url)

        return None

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']

