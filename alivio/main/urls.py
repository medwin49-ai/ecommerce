from django.urls import  path
from . import views

urlpatterns = [
    path("" , views.index , name="index"),
    path("products/<str:product_name>" , views.product, name="products" ),
    path("shopping-cart", views.shopping_cart_page, name="shopping-cart"),
    path("add-cart-from-home", views.add_to_cart_from_home, name="cart-home"),
]