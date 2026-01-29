from django.contrib import admin
from .models import Product, ProductImage,Cart,CartItem,CakeOrder


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'treat_type', 'flavor', 'price', 'rating', 'popularity')
    list_filter = ('treat_type', 'flavor')
    search_fields = ('name',)
admin.site.register(CartItem)
 
 