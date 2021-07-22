from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect ,reverse
from django.http import HttpResponse ,  HttpResponseRedirect
from .models import *
from .forms import CartForm , CartQuantityItem , DeleteButton


def index(response):
    products = Product.objects.all()
    potencies = []

    for product in products:
        p = list(Potency.objects.filter(product_id=product.id).order_by('potency_value'))
        potencies.append(p)

    return render(response, "main/main.html", {'products': zip(products, potencies)})


def product(request, product_name):
    product = get_object_or_404(Product , product_name=product_name)
    potencies = get_list_or_404(Potency , product_id = product.id ) 
    
    choices = []
    for i in potencies:
        add_tuple = (i.id , str(i.potency_value) + "mg")
        choices.append(add_tuple)

    if request.method == 'POST':
        form = CartForm(request.POST)
        form.fields["potency"].choices = choices

        if form.is_valid():
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)   
            potency = form.cleaned_data['potency']
            quantities = form.cleaned_data['quantity']
            
            potency = Potency.objects.get(id=potency)
           
            orderItem, created = OrderItem.objects.get_or_create(order = order , potency = potency)
            orderItem.quantity = quantities
            orderItem.save()
            
            return HttpResponseRedirect('/shopping-cart')
        else:
            form = CartForm()
            form.fields["potency"].choices = choices    

    else:
        form = CartForm()
        form.fields["potency"].choices = choices
        return render(request, "main/product.html", { 'form':form, 'product': product, 'potencies': potencies,})


def shopping_cart_page(response):
    
    device = response.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    if response.method == "POST":
        
        form = CartQuantityItem(response.POST)
    
        if form.is_valid():        
           
            quantity_delta = form.cleaned_data['btn']
            potency = form.cleaned_data['potency']
            order_item, created = OrderItem.objects.get_or_create(order = order , potency = potency)
                      
            if order_item.quantity + quantity_delta  == 0:
                return HttpResponseRedirect('/shopping-cart')
            
            else:
                order_item.quantity = order_item.quantity + quantity_delta
                order_item.save()
                return HttpResponseRedirect('/shopping-cart')
    
        delete_form = DeleteButton(response.POST)
        
        print(delete_form)
        if delete_form.is_valid(): 
            potency = form.cleaned_data['potency']
            order_item, created = OrderItem.objects.get_or_create(order = order , potency = potency)
            order_item.delete()
            
            return HttpResponseRedirect('/shopping-cart')

        else:
            form = CartQuantityItem()
            delete_form = DeleteButton()
        
    else:
        form = CartQuantityItem()
        delete_form = DeleteButton()
    
        
    return render(response, 'main/shopping-cart.html', {'order' : order , 'form' : form , 'delete_form' : delete_form, })


def checkout_page(response):
    device = response.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

        
    return render(response, 'main/checkout.html', {'order' : order , })