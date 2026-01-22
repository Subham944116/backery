from rest_framework import serializers
from .models import User, UserProfile


class RegisterSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    full_name = serializers.CharField()
    email = serializers.EmailField()
    address = serializers.CharField()
    pincode = serializers.CharField(max_length=6)
    city = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.get(mobile=validated_data['mobile'])

        profile = UserProfile.objects.create(
            user=user,
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            address=validated_data['address'],
            pincode=validated_data['pincode'],
            city=validated_data['city']
        )
        return profile



class SendOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)


class VerifyOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']
