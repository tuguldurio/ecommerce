from rest_framework import serializers
from . import models


class ProductSerializer(serializers.ModelSerializer):
    images =  serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Product
        fields = ('id' ,'name', 'images', 'price')

    def to_representation(self, obj):
        data = super().to_representation(obj)
        images = [img.thumbnail() for img in obj.images.all()]
        
        data['images'] = images
        return data

class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()