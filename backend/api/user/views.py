from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ( 
    RegisterSerializer, 
    TokenObtainPairSerializer, CookieTokenRefreshSerializer, 
    PasswordResetSerializer
)

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from api.user.models import User
from api.product.models import Product
from api.cart.models import CartProduct

from api.cart.utils import get_user_cart


class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=serializer.validated_data['email']).exists():
            return Response({'detail': 'User with the email already exists!'}, 409)

        user = serializer.save()

        # When user shops before creating an account
        # All those product which saved in cookies will be saved in database
        # Not an actual registration process
        data = serializer.validated_data
        if 'products' in data:
            cart = get_user_cart(user.id)
            for prod in data['products']:
                try:
                    product = Product.objects.get(id=prod['product_id'])
                    cart_product = CartProduct(cart_id=cart.id, product_id=product.id, quantity=prod['quantity'])
                    cart_product.save()
                except Product.DoesNotExist:
                    return Response({'detail': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


class Logout(APIView):
    def post(self, request):
        res = Response()
        res.delete_cookie('refreshToken')
        return res 

cookie_max_age = 3600 * 24 * 14 # 14 days


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            response.set_cookie('refreshToken', response.data['refresh'], max_age=cookie_max_age, httponly=True, samesite='strict')
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = TokenObtainPairSerializer


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            response.set_cookie('refreshToken', response.data['refresh'], max_age=cookie_max_age, httponly=True, samesite='strict')
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer


class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response()