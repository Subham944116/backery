from django.db import models

from django.utils import timezone

# Create your models here.
 
class Product(models.Model):
 
    CATEGORY_CHOICES = [

        ('cake', 'Cake'),

        ('cookie', 'Cookie'),

        ('treat', 'Treat'),

    ]
 
    FLAVOUR_CHOICES = [

        ('chocolate', 'Chocolate'),

        ('strawberry', 'Strawberry'),

        ('vanilla', 'Vanilla'),

        ('mango', 'Mango'),

        ('red_velvet', 'Red Velvet'),

    ]
 
    WEIGHT_CHOICES = [

        (0.1, '0.1 Kg'),

        (0.5, '0.5 Kg'),

        (1, '1 Kg'),

        (1.5, '1.5 Kg'),

        (2, '2 Kg'),

    ]

    DIET_CHOICES = [
        ('Vegan', 'Vegan'),

        ('Gluten-Free', 'Gluten-Free'),

        ('Sugar-Free', 'Sugar-Free'),

        ('Vegetarian', 'Vegitarian'),

        ('Non-Vegetarian', 'Non-Vegitarian'),
    ]
 
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    flavour = models.CharField(max_length=30, choices=FLAVOUR_CHOICES)
    weight = models.FloatField(choices=WEIGHT_CHOICES)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(
    default=timezone.now
)
    is_vegetarian = models.BooleanField(default=False)

    # image = models.ImageField(upload_to='products/', blank=True, null=True)
    # dietary options
    
    diet_type = models.CharField(
        max_length=20,
        choices=DIET_CHOICES,
        default=''
    )
 
    def __str__(self):

        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    def __str__(self):
        return self.product.name