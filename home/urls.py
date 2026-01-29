from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomePageAPIView.as_view(), name='home-page'),
]
