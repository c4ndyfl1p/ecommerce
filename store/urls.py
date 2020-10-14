from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"), 
     path('product/', views.product, name="product"),  
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),  
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
]