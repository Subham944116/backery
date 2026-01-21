from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']

            user, created = User.objects.get_or_create(
                mobile=mobile,
                defaults={'username': mobile}
            )

            otp = OTP.objects.create(user=user)

            return Response({
                "message": "OTP sent successfully",
                "otp": otp.code   # RETURN OTP (NO SMS)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile = serializer.validated_data['mobile']
            otp_code = serializer.validated_data['otp']

            try:
                user = User.objects.get(mobile=mobile)
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

                return Response({
                    "message": "OTP verified successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=200)

            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

        return Response(serializer.errors, status=400)
