from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),  
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),  
    path('checkout/', views.checkout, name="checkout"),
    path('cart/', views.cart, name="cart"),
    path('update_item/', views.updateItem, name="update_item"),
]