from django.urls import path
from .views import*

urlpatterns = [
    path('create/', CakeCreateView.as_view()),
    path('add-to-cart/<int:order_id>/', AddCustomCakeToCartView.as_view()),
]
