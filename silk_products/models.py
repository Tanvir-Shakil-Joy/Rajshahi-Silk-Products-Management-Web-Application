from django.db import models

class SilkProduct(models.Model):
    PRODUCT_TYPES = [
        ('saree', 'Saree'),
        ('fabric', 'Fabric'),
        ('scarf', 'Scarf'),
    ]

    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
