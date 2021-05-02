
from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()
    featured = models.BooleanField(default=False)
    in_stock = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='images')
    path = models.ImageField(upload_to='images/')

    def thumbnail(self):
        if settings.DEBUG:
            return 'http://192.168.0.235:8000'+settings.MEDIA_URL+str(self.path)
        return str(self.path)