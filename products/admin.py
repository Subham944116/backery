# products/admin.py
from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3   # how many image upload boxes to show
    min_num = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    inlines = [ProductImageInline]

# Optional: hide ProductImage from sidebar
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
