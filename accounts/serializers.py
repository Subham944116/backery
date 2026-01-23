from rest_framework import serializers
from .models import *


class SendOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)


class VerifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if instance.profile_image and request:
            data['profile_image'] = request.build_absolute_uri(
                instance.profile_image.url
            )
        return data
