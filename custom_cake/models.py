from django.db import models

from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class CakeOrder(models.Model):

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('vanilla', 'Vanilla'),
        ('strawberry', 'Strawberry'),
        ('butterscotch', 'Butterscotch'),
    ]

    SHAPE_CHOICES = [
        ('round', 'Round'),
        ('square', 'Square'),
        ('heart', 'Heart'),
    ]

    COLOR_CHOICES = [
        ('pink', 'Pink'),
        ('mint', 'Mint'),
        ('lavender', 'Lavender'),
        ('buttercream', 'Buttercream'),
    ]

    PRICE_MAP = {
        '0.5': 500,
        '1': 900,
        '2': 1700,
        '3': 2500,
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flavor = models.CharField(max_length=50, choices=FLAVOR_CHOICES)
    weight = models.CharField(max_length=5)  # 0.5,1,2,3
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)

    message = models.TextField(blank=True)
    image = models.ImageField(upload_to='cake_refs/', blank=True, null=True)

    delivery_date = models.DateField()
    delivery_time = models.TimeField()

    total_price = models.PositiveIntegerField(default=0)
     

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.PRICE_MAP.get(self.weight, 0)
        super().save(*args, **kwargs)
