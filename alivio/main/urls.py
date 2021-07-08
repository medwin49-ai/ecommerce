from django.urls import  path
from . import views

urlpatterns = [
    path("" , views.index , name="index"),
    path("products/<str:product_name>" , views.product_page, name="products" ),
    path("shopping-cart", views.shopping_cart_page, name="shopping-cart"),
]