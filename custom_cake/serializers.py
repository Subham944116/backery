from rest_framework import serializers
from .models import CakeOrder

class CakeOrderSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = CakeOrder
        fields = '__all__'
        read_only_fields = [
            'user',
            'total_price',
            'created_at'
        ]

 