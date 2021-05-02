from django.db import models
from api.user.models import User
from api.product.models import Product


class Order(models.Model):
    STATUSES = (
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=STATUSES, default='pending')
    amount = models.PositiveIntegerField()


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()