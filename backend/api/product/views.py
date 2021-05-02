from rest_framework import status
from rest_framework import generics
from rest_framework import permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from api.product.models import Product
from api.product.serializers import ProductSerializer, IdSerializer


class Products(generics.ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

class ProductDetail(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise NotFound
        
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class FtdProducts(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.filter(featured=True)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)