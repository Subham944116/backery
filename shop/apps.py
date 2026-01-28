from django.apps import AppConfig


<<<<<<<< HEAD:address/apps.py
class AddressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'address'
========
class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
>>>>>>>> 236d578ddcb1010705e5843df71f4b4e4912c72f:shop/apps.py
