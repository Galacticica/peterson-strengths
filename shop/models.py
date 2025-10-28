from django.db import models
import os
from django.conf import settings


def product_image_path(instance, filename):
    """Upload product images to static/public/products/"""
    return os.path.join('products', filename)


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    monthly = models.BooleanField(default=False)

    def __str__(self):
        return self.name
