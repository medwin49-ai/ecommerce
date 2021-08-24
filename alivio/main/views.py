from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect ,reverse
from django.http import JsonResponse ,  HttpResponseRedirect , HttpResponse
from .models import *
from .forms import CartForm, CartQuantityItem, DeleteButton, HomeCartForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import json
import stripe


stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

def index(request):
    products = Product.objects.all()
    potencies = []

    for product in products:
        p = list(Potency.objects.filter(product_id=product.id).order_by('potency_value'))
        potencies.append(p)
    
    try:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except KeyError:
        return render(request, "main/main.html", {'products': zip(products, potencies), 'order_items': 0 })

    
    return render(request, "main/main.html", {'products': zip(products, potencies), 'order_items' : order.get_cart_quantity })


def add_to_cart_from_home(request):
    if request.method == "POST":
        form = HomeCartForm(request.POST)
        print("in form")
        if form.is_valid():
            print("form was valid")
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)   
            potency = form.cleaned_data['potency']
            print("potency", 1)
            quantity = 1
            
            potency = Potency.objects.get(id=potency)
           
            orderItem, created = OrderItem.objects.get_or_create(order = order , potency = potency)
            orderItem.quantity = quantity
            orderItem.save()
            return HttpResponseRedirect("/shopping-cart")
        else:
            return HttpResponseRedirect("")

    return HttpResponseRedirect("")


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
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        return render(request, "main/product.html", { 'form':form, 'product': product, 'potencies': potencies, 'order_items' : order.get_cart_quantity })


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
    
        
    return render(response, 'main/shopping-cart.html', {'order' : order , 'form' : form , 'delete_form' : delete_form, 'order_items': order.get_cart_quantity })


def checkout_page(response):
    
    device = response.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    if order.get_cart_total == 0:
        return HttpResponseRedirect('/shopping-cart')
        
    return render(response, 'main/checkout.html', {'order' : order , 'order_items': order.get_cart_quantity})


def create_payment_intent(response):
    try:
        response_json = json.loads(response.body)
        order = Order.objects.get(id=response_json['order'])
        device = response.COOKIES['device']

        customerName = response_json['firstName'].strip() + " " + response_json['lastName'].strip()

        customer_id = None

        # Try to find exsisting customer. If found, update device field with current device.
        try:
            customer = Customer.objects.get(name=customerName, email=response_json['email'].strip())
            oldCustomer = Customer.objects.get(device=device)

            customer.device = oldCustomer.device
            order.customer = customer

            customer.save()
            order.save()
            oldCustomer.delete()

            customer_id = customer.stripe_id

        # Exsisting customer was not found, update current customer placeholder with correct information
        except Customer.DoesNotExist:
            customer = stripe.Customer.create(
                email = response_json['email'].strip(), 
                name = customerName,
                shipping = {'address': {'city': response_json['city'].strip(), 'country': 'US',
                                        'line1': response_json['address1'].strip(), 'line2': response_json['address2'].strip(),
                                        'postal_code': response_json['zip'].strip(), 'state': response_json['state'].strip()},
                            'name': customerName}
            )

            updateCustomer = Customer.objects.get(device=device)
            updateCustomer.name = customerName
            updateCustomer.email = response_json['email'].strip()
            updateCustomer.stripe_id = customer['id']
            updateCustomer.save()

            customer_id = customer['id']

        intent = stripe.PaymentIntent.create(
            amount = int(100 * order.get_cart_total),
            currency = 'usd',
            customer = customer_id,
            metadata = {
                "device": response.COOKIES['device']
            }
        )


        return JsonResponse({
            'clientSecret': intent['client_secret']
        })

        
    except Exception as e:
        print("Error in create_payment_intent: " + e)
        return JsonResponse({ 'error': str(e) })


def success_page(response):
    return render(response, 'main/success.html', {} )

@csrf_exempt
def stripe_webhook(request):


    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
      # Handle the checkout.session.completed event
    # if event['type'] == 'checkout.session.completed':
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
        event_dict = event.to_dict()
        intent = event_dict['data']['object']
        device = intent['charges']['data'][0]['metadata']['device']
        customer, created = Customer.objects.get_or_create(device=device)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order.complete = True
        order.save()
        print(order.complete)

        return redirect('shopping-cart')
        # session = event['data']['object']
        # customer_email = session["customer_details"]["email"]
        # product_id = session["metadata"]["product_id"]
        # product = Product.objects.get(id=product_id)
        # TODO - send an email and make oder complete.

    return HttpResponse(status=200)


