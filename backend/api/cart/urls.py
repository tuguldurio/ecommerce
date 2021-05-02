from django.urls import path
# from api.core import views
from . import views

urlpatterns = [
    path('cart', views.CartView.as_view()),
    path('cart/products/<int:product_id>', views.CartSlugView.as_view())
]