from django.urls import path
from .views import *

urlpatterns = [
    path('send-otp/', SendOTPView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),
    path('profile/', UserProfileView.as_view()),
]

