from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class SilkProduct(models.Model):
    TYPE_CHOICES = [
        ('saree', 'Saree'),
        ('fabric', 'Fabric'),
        ('scarf', 'Scarf'),
        ('shawl', 'Shawl'),
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
