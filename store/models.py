from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # onetoone means a user can have only one customer and a cust can have only one user
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    @receiver(post_save, sender=User)
    def create_user_customer(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_customer(sender, instance, **kwargs):
        instance.customer.save()

    def __str__(self):
         return self.user.username

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=5000, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    fandom_good = models.BooleanField(default=False, null=True, blank=False)
    home_decor = models.BooleanField(default=False, null=True, blank=False)
    coaster = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

    @property
    # expensive try if == undefined
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,  null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null = True)

    @property
    def get_cart_total(self):

        orderitems = self.orderitem_set.all()
        # where is "orderitem_set.all() coming from?"
        total = sum([item.get_total for item in orderitems])
        return total

    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        # if isinstance(self.quantity, type(None)):
        #     self.quantity = 0
        total = sum([item.quantity for item in orderitems])
        return total



    def __str__(self):
        return str(self.transaction_id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        # if self.quantity is None:
        #     self.quantity = 0
        total = self.product.price * self.quantity
        return int(total)

class WishlistOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,  null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null = True)

    @property
    def get_cart_total(self):

        orderitems = self.wishlistorderitem_set.all()
        # where is "orderitem_set.all() coming from?"
        total = sum([item.get_total for item in orderitems])
        return total

    def get_cart_items(self):
        orderitems = self.wishlistorderitem_set.all()
        # if isinstance(self.quantity, type(None)):
        #     self.quantity = 0
        total = sum([item.quantity for item in orderitems])
        return total


    def __str__(self):
        return str(self.transaction_id)


class WishlistOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(WishlistOrder, on_delete = models.SET_NULL, null=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        # if self.quantity is None:
        #     self.quantity = 0
        total = self.product.price * self.quantity
        return int(total)
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=200, null=True)
    reference = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

