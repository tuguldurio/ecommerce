from rest_framework import serializers

from .models import Order


class OrdersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'created_at', 'status', 'amount')