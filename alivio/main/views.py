from django.shortcuts import render
from django.http import HttpResponse

from .models import Potency, Product


def index(response):
    products = Product.objects.all()
    potencies = []

    for product in products:
        p = list(Potency.objects.filter(product_id=product.id).order_by('potency_value'))
        potencies.append(p)

    return render(response, "main/main.html", {'products': zip(products, potencies)})


def product_page(response):
    return render(response, "main/product.html", {})

