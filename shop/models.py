from custom_cake.models import CakeOrder
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):

    TREAT_TYPE_CHOICES = [
        ('cake', 'Cake'),
        ('cookie', 'Cookie'),
    ]

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('strawberry', 'Strawberry'),
        ('vanilla', 'Vanilla'),
        ('mango', 'Mango'),
        ('red_velvet', 'Red Velvet'),
    ]

    name = models.CharField(max_length=150)
    description = models.TextField()
    treat_type = models.CharField(max_length=10, choices=TREAT_TYPE_CHOICES)
    flavor = models.CharField(max_length=20, choices=FLAVOR_CHOICES)

    weight = models.DecimalField(max_digits=3, decimal_places=2)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField(default=0)

    options = models.JSONField(default=list)
    popularity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ✅ ADD THIS MODEL
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} Image"



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"



class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    custom_cake = models.ForeignKey(
        CakeOrder,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        if self.product:
            return self.product.price * self.quantity
        if self.custom_cake:
            return self.custom_cake.total_price
        return 0



