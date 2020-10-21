from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail 

# Create your views here.
def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # when user is not logged on. Creating manual 0 values
        # so no error is thrown
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = 0

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # when user is not logged on. Creating manual 0 values
        # so no error is thrown
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = 0

    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # when user is not logged on. Creating manual 0 values
        # so no error is thrown
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems= 0

    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    #resolves the error while adding new products
    if orderItem.quantity is None:
        orderItem.quantity = 0

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
	

    return JsonResponse('Item was added', safe=False)
    
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, help_text='Enter your first name')
    email = forms.EmailField(max_length=64, help_text='Enter a valid email address')
    

    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        fields = UserCreationForm.Meta.fields + ('first_name', 'email',)


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            first_name = form.data.get('first_name')
            email = form.cleaned_data.get('email')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)

            subject = 'welcome to Jar-3D-Wale!!'
            message = f'Hi {first_name},\nThank you for registering on JARThreeDeeWale!! \nEnjoy shopping on our site!'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email, ] 
            send_mail( subject, message, email_from, recipient_list ) 

            return redirect("/")

            

            
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            

    form = SignUpForm
    context = {'form': form}
    return render(request, "store/register.html", context)
                    
def logout_request(request):
    logout(request)
    return redirect("/")
    # messages.info(request, "logged out succesfully")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")
        else:
                messages.error(request, "Invalid username or password")


    form = AuthenticationForm()
    context = {'form': form}
    return render(request, "store/login.html", context)
