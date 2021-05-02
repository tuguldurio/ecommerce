from rest_framework import serializers
# from . import models

class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartSlugSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)