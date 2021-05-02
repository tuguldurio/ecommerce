from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from api.cart.models import CartProduct
from api.cart.serializers import CartSerializer, CartSlugSerializer

from api.product.models import Product, ProductImage
from api.cart.utils import get_user_cart


class CartView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ''' Get all products in cart '''
        cart = get_user_cart(request.user.id)
        cart_products = CartProduct.objects.filter(cart_id=cart.id).order_by('id').all()
        data = []

        for cart_product in cart_products:
            product = Product.objects.get(id=cart_product.product.id)
            data.append({
                'id': product.id,
                'name': product.name,
                'image': ProductImage.objects.filter(product_id=product.id).first().thumbnail(),
                'unit_price': product.price,
                'quantity': cart_product.quantity
            })

        return Response(data)

    def post(self, request):
        serializer = CartSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        cart = get_user_cart(request.user.id)

        for query in serializer.data:
            cart_product = CartProduct(cart_id=cart.id, product_id=query['product_id'], quantity=query['quantity'])
            cart_product.save()

        return Response()


class CartSlugView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, product_id):
        ''' Creates product in cart '''
        serializer = CartSlugSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        cart = get_user_cart(request.user.id)

        # error if amount of product exceeds that of in stock
        product = Product.objects.get(id=product_id)
        if data['quantity'] > product.in_stock:
            return Response(f'Sorry, we only have {product.in_stock} left in stock', status=status.HTTP_400_BAD_REQUEST)

        try:
            # get cart if user has product in cart already
            cart_product = CartProduct.objects.get(cart_id=cart.id, product_id=product_id)
            cart_product.quantity += data['quantity']
        except CartProduct.DoesNotExist:
            # otherwise create product
            cart_product = CartProduct(cart_id=cart.id, product_id=product_id, quantity=data['quantity'])

        # if user tries to add more
        if cart_product.quantity > product.in_stock:
            return Response('You already added maximum ammount', status=status.HTTP_400_BAD_REQUEST)

        cart_product.save()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, product_id):
        ''' Updates product in cart '''
        serializer = CartSlugSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        cart = get_user_cart(request.user.id)

        # error if amount of product exceeds that of in stock
        product = Product.objects.get(id=product_id)
        if data['quantity'] > product.in_stock:
            return Response(f'Sorry, we only have {product.in_stock} left in stock', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_product = CartProduct.objects.get(cart_id=cart.id, product_id=product_id)
            cart_product.quantity = data['quantity']
            cart_product.save()
        except CartProduct.DoesNotExist:
            return Response('Product not found in cart', status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, product_id):
        ''' Deletes product from cart '''
        cart = get_user_cart(request.user.id)

        try:
            cart_product = CartProduct.objects.get(cart_id=cart.id, product_id=product_id)
            cart_product.delete()
        except CartProduct.DoesNotExist:
            return Response('Product not found in cart', status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)