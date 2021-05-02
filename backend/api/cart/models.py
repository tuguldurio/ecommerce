from django.db import models

# from api.user.models import User
from api.product.models import Product


class Cart(models.Model):
    user = models.OneToOneField('api.User', on_delete=models.CASCADE)
    

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()