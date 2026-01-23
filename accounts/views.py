from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser

from .models import User, OTP, UserProfile
from .serializers import SendOTPSerializer, VerifyOTPSerializer, UserProfileSerializer


 
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        # ✅ CREATE USER IF NOT EXISTS
        user, created = User.objects.get_or_create(
            mobile=mobile,
            defaults={"username": mobile}
        )

        # ✅ CREATE PROFILE IF NOT EXISTS (MOBILE ONLY)
        UserProfile.objects.get_or_create(
            user=user,
            defaults={"mobile": mobile}
        )

        # ✅ CREATE OTP
        otp = OTP.objects.create(
            user=user,
            mobile=mobile
        )

        return Response(
            {
                "message": "OTP sent successfully",
                "mobile": mobile,
                "otp": otp.code,  # ⚠ DEV ONLY
                "new_user": created
            },
            status=status.HTTP_200_OK
        )


 
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        otp_code = serializer.validated_data["otp"]

        otp = OTP.objects.filter(
            mobile=mobile,
            code=otp_code,
            is_verified=False
        ).last()

        if not otp:
            return Response(
                {"error": "Invalid OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if otp.is_expired():
            return Response(
                {"error": "OTP expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark OTP as verified
        otp.is_verified = True
        otp.save()

        user = otp.user
        refresh = RefreshToken.for_user(user)

        profile = UserProfile.objects.get(user=user)

        # Check if profile is complete (mobile, full_name, email)
        profile_completed = bool(
            profile.mobile and profile.full_name and profile.email
        )

        # Build response
        response_data = {
            "message": "OTP verified successfully",
            "token": str(refresh.access_token),
            "profile_completed": profile_completed
        }

        # ✅ Include fields only if profile is NOT complete
        if not profile_completed:
            response_data.update({
                "full_name": profile.full_name or "required for profile completion ",
                "email": profile.email or "rrequired for profile completion"
            })

        return Response(response_data, status=status.HTTP_200_OK)



 
class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser,MultiPartParser, FormParser]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(
            profile,
            context={"request": request}
        )
        return Response(serializer.data)

    def patch(self, request):
        profile = UserProfile.objects.get(user=request.user)

        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
