from rest_framework import serializers
from .models import *


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'address_type',
            'name',
            'email',
            'phone_number',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'pincode',
            'latitude',
            'longitude',
            'is_default',
            'created_at',
        ]
        read_only_fields = ['id', 'is_default', 'created_at']


class SetDefaultAddressSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()

    def validate_address_id(self, value):
        user = self.context['request'].user
        if not Address.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError("Address not found.")
        return value

    def save(self):
        user = self.context['request'].user
        address_id = self.validated_data['address_id']

        Address.objects.filter(user=user, is_default=True).update(is_default=False)
        Address.objects.filter(id=address_id, user=user).update(is_default=True)

        return {"message": "Default address updated"}
