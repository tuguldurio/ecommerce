import json
import stripe
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from api.user.models import User
from api.product.models import Product
from api.cart.models import CartProduct
from .models import Order, OrderProduct
from .serializers import OrdersListSerializer
from api.cart.utils import get_user_cart

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # details about cart products
        cart = get_user_cart(request.user.id)
        cart_products = CartProduct.objects.filter(cart_id=cart.id).all()
        line_items = []
        for cart_product in cart_products:
            product = Product.objects.get(id=cart_product.product.id)
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': product.price,
                    'product_data': {
                        'name': product.name,
                        # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        'metadata': {'product_id': product.id}
                    },
                },
                'quantity': cart_product.quantity
            })

        # Domain for the success and cancel view
        if settings.DEBUG:
            CLIENT_DOMAIN = 'http://192.168.0.235:8080'
        else:
            CLIENT_DOMAIN = 'https://domain.com'
        
        session = stripe.checkout.Session.create(
            billing_address_collection='auto',
            shipping_address_collection={
                'allowed_countries': ['US'],
            },
            payment_method_types=['card'],
            mode='payment',
            line_items=line_items,
            customer_email=request.user.email,
            success_url= CLIENT_DOMAIN+'/success',
            cancel_url=CLIENT_DOMAIN,
        )

        return Response({
            'sessionId': session.id,
            'publicKey': settings.STRIPE_PUBLIC_KEY
        })

webhook_secret = settings.STRIPE_WEBHOOK

class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as e:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=400)
        
        if event.type == 'checkout.session.completed':
            session = event.data.object # contains a stripe.PaymentIntent
            line_items = stripe.checkout.Session.list_line_items(session.id)
            
            user = User.objects.get(email=event.data.object.customer_email)

            # Fullfil order of user
            order = Order(user=user)
            order.amount = session.amount_total
            order.save()

            for item in line_items.data:
                product_id = int(stripe.Product.retrieve(item.price.product).metadata['product_id'])
                product = Product.objects.get(id=product_id)
                # Create product for the order
                order_product = OrderProduct(order=order, product=product, quantity=item.quantity)
                order_product.save()
                # Decreases the available stock numbers
                product.in_stock -= item.quantity
                product.save()

            # Clear cart for user
            cart = get_user_cart(user.id)
            cart_products = cart.cartproduct_set.all()
            for cart_product in cart_products:
                cart_product.delete()

        return Response(status=200)


class OrdersView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = OrdersListSerializer

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user_id=user.id)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)