from django.urls import  path
from . import views

urlpatterns = [
    path("" , views.index , name="index"),
    path("product", views.product_page, name="product" ),
    path("shopping-cart", views.shopping_cart_page, name="shopping-cart"),
]