from django.urls import path
from .views import *

urlpatterns = [
    path('products_list/', ProductCreateAPIView.as_view()),
]
