from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import ( 
    TokenObtainPairSerializer as ObtainSerializer, TokenRefreshSerializer
)
# from api.cart.serializers import CartSerializer

from .models import User

class RegisterCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    password = serializers.CharField()
    products = RegisterCartSerializer(many=True, required=False)

    class Meta:
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('password must be atleast 8 character')
        return password
        
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['firstname'], validated_data['lastname'], password=validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'firstname', 'lastname']


class TokenObtainPairSerializer(ObtainSerializer):
    default_error_messages = {
        'no_active_account': 'Wrong email or password!'
    }


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refreshToken')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refreshToken\'')


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    def validate(self, attrs):
        try:
            email = attrs['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                
        except:
            pass
        return super().validate(attrs)