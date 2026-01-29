from rest_framework import serializers
from shop.models import CakeOrder

class OrderHistorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CakeOrder
        fields = [
            'id',
            'flavor',
            'weight',
            'shape',
            'color',
            'message',
            'image_url',
            'delivery_date',
            'delivery_time',
            'total_price',
            'created_at',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
