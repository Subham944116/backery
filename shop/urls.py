from django.urls import path
from .views import (
    ProductListView,
    AddToCartView,
    CartView,
    OrderNowView
)

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('cart/add/', AddToCartView.as_view()),   # prebuilt cake
    path('cart/', CartView.as_view()),             # view full cart
    path('order-now/', OrderNowView.as_view()),    # single item checkout
]
