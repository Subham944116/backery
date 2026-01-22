from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser


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
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Registration completed"},
            status=status.HTTP_201_CREATED
        )




class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        user = User.objects.filter(mobile=mobile).first()

        # 🔹 If new mobile → create user
        if not user:
            user = User.objects.create_user(
                mobile=mobile,
                username=mobile,
                password=None
            )

        otp = OTP.objects.create(user=user)

        is_registered = UserProfile.objects.filter(user=user).exists()

        return Response(
            {
                "message": "OTP sent successfully",
                "mobile": mobile,
                "otp": otp.code,             # ⚠ DEV ONLY
                "is_registered": is_registered
            },
            status=status.HTTP_200_OK
        )






class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        otp_code = serializer.validated_data['otp']

        user = User.objects.filter(mobile=mobile).first()
        if not user:
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

        is_registered = UserProfile.objects.filter(user=user).exists()

        return Response(
            {
                "message": "OTP verified successfully",
                "mobile": mobile,
                "is_registered": is_registered,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_200_OK
        )





class UserProfileDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileSerializer(
            profile,
            context={'request': request}
        )
        return Response(serializer.data)

    def patch(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
