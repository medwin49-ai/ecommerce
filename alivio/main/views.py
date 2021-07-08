from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.http import HttpResponse

from .models import Potency, Product


def index(response):
    products = Product.objects.all()
    potencies = []

    for product in products:
        p = list(Potency.objects.filter(product_id=product.id).order_by('potency_value'))
        potencies.append(p)

    return render(response, "main/main.html", {'products': zip(products, potencies)})


def product_page(response , product_name):
        product = get_object_or_404(Product , product_name=product_name)
        potencies = get_list_or_404(Potency , product_id = product.id )
        return render(response, "main/product.html", {'product': product, 'potencies': potencies})


def shopping_cart_page(response):
    return render(response, "main/shopping-cart.html", {})