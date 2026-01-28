from django.db import models

# Create your models here.

class HomeHero(models.Model):
    badge_text = models.CharField(max_length=100, default="Freshly Baked Daily")
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    hero_image = models.ImageField(upload_to="home/hero/")
    primary_button_text = models.CharField(max_length=50, default="Order Now")
    secondary_button_text = models.CharField(max_length=50, default="View Menu")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class HomeCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="home/categories/")
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    TREAT_CHOICES = (
        ('cake', 'Cake'),
        ('cookie', 'Cookie'),
        ('healthy', 'Healthy'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    treat_type = models.CharField(max_length=20, choices=TREAT_CHOICES)
    rating = models.FloatField(default=0)
    is_featured = models.BooleanField(default=False)  # ⭐ FOR HOME PAGE
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} Image"
