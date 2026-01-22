from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, OTP, UserProfile
from .serializers import (
    RegisterSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    UserProfileSerializer
) 


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)

        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']

            try:
                user = User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid mobile number, please register first"},
                    status=400
                )

            otp = OTP.objects.create(user=user)

            return Response(
                {
                    "message": "OTP sent successfully",
                    "otp": otp.code  # DEV ONLY
                },
                status=200
            )

        return Response(serializer.errors, status=400)





class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            otp_code = serializer.validated_data['otp']

            try:
                user = User.objects.get(mobile=mobile)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            otp = OTP.objects.filter(
                user=user,
                code=otp_code,
                is_verified=False
            ).last()

            if not otp:
                return Response({"error": "Invalid OTP"}, status=400)

            if otp.is_expired():
                return Response({"error": "OTP expired"}, status=400)

            otp.is_verified = True
            otp.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=200
            )

        return Response(serializer.errors, status=400)


class UserProfileDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        try:
            profile = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            profile = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated", "data": serializer.data}
            )
        return Response(serializer.errors, status=400)

    def patch(self, request, id):
        try:
            profile = UserProfile.objects.get(id=id)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileSerializer(
            profile, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Profile updated", "data": serializer.data}
            )
        return Response(serializer.errors, status=400)

