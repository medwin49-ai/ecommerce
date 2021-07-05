from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return render(response, "main/main.html", {})

def product_page(response):
    return render(response, "main/product.html", {})