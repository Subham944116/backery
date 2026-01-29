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

# serializers.py (ADD BELOW existing serializers)

class ProductDetailSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    available_weights = serializers.SerializerMethodField()
    available_flavors = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'treat_type',
            'flavor',
            'weight',
            'rating',
            'images',
            'available_weights',
            'available_flavors',
        ]

    def get_images(self, obj):
        request = self.context.get('request')
        images = []

        for img in obj.images.all():
            if img.image and request:
                images.append({
                    "url": request.build_absolute_uri(img.image.url),
                    "is_primary": img.is_primary
                })

        return images

    def get_available_weights(self, obj):
        # frontend buttons: 0.5kg, 1kg, 2kg
        return ["0.5kg", "1kg", "2kg"]

    def get_available_flavors(self, obj):
        return [
            {"label": "Chocolate", "value": "chocolate"},
            {"label": "Vanilla", "value": "vanilla"},
            {"label": "Strawberry", "value": "strawberry"},
            {"label": "Butterscotch", "value": "butterscotch"},
        ]
