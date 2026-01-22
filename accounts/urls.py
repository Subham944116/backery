from django.urls import path
from .views import (
    SendOTPView,
    VerifyOTPView,
    RegisterView,
    UserProfileDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('profile/<int:id>/', UserProfileDetailView.as_view()),
]
