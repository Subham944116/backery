from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.authtoken.models import Token

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
            return Response({"error": "Invalid OTP"}, status=400)

        if otp.is_expired():
            return Response({"error": "OTP expired"}, status=400)

        otp.is_verified = True
        otp.save()

        user = otp.user

        # ✅ DRF TOKEN (NOT JWT)
        token, created = Token.objects.get_or_create(user=user)

        profile = UserProfile.objects.get(user=user)

        profile_completed = bool(
            profile.mobile and profile.full_name and profile.email
        )

        response_data = {
            "message": "OTP verified successfully",
            "token": token.key,
            "profile_completed": profile_completed
        }

        if not profile_completed:
            response_data.update({
                "full_name": "required for profile completion",
                "email": "required for profile completion"
            })

        return Response(response_data, status=200)


 
class UserProfileView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser,MultiPartParser, FormParser]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(
            profile,
            context={"request": request}
        )
        return Response(serializer.data,status=status.HTTP_200_OK)

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
        return Response(serializer.data,status=status.HTTP_201_CREATED)
