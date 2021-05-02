from django.urls import path
from api.order import views

urlpatterns = [
    path('order/create-checkout-session', views.CreateCheckoutSessionView.as_view()),
    path('order/stripe_webhook', views.StripeWebhookView.as_view()),
    path('orders', views.OrdersView.as_view())
]