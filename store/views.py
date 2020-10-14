from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)
#view product

def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/product.html', context)


#Authentication
def login(request):
    return render(request, 'store/login.html')

def signup(request):
    return render(request, 'store/signup.html')


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # when user is not logged on. Creating manual 0 values
        # so no error is thrown
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order': order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # when user is not logged on. Creating manual 0 values
        # so no error is thrown
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order': order}
    return render(request, 'store/checkout.html', context)
