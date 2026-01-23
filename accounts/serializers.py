from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['mobile', 'password', 'email', 'username']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # 1. Create the user first
        user = User.objects.create_user(
            mobile=validated_data['mobile'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            username=validated_data.get('username', '')
        )

        # 2. Create profile only if it doesn't exist
        UserProfile.objects.get_or_create(user=user)

        return user


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

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image:
            if request:
                return request.build_absolute_uri(obj.profile_image.url)
            return obj.profile_image.url
        return None


