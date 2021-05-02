from django.urls import path
from . import views

urlpatterns = [
    path('products/all', views.Products.as_view()),
    path('products/<int:id>', views.ProductDetail.as_view()),
    path('products/featured', views.FtdProducts.as_view())
]