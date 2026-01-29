from django.contrib import admin
from .models import HomeHero, HomeCategory, Product, ProductImage

@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active',)

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            HomeHero.objects.exclude(id=obj.id).update(is_active=False)
        super().save_model(request, obj, form, change)


@admin.register(HomeCategory)
class HomeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'treat_type', 'price', 'is_featured')
    list_editable = ('is_featured',)
    list_filter = ('treat_type', 'is_featured')
    inlines = [ProductImageInline]
