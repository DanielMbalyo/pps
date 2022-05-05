from decimal import Decimal
from django.conf import settings
from django.shortcuts import reverse, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete

from src.product.models import Product, UserProduct

User = settings.AUTH_USER_MODEL

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)

    def __str__(self):
        return self.product.product.title

    def save(self, *args, **kwargs):
        qty = self.quantity
        if int(qty) >= 1:
            price = self.product.sale_price
            self.product_total = Decimal(qty) * Decimal(price)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.subtotal += instance.product_total
post_save.connect(cart_item_post_save_receiver, sender=CartItem)
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
            return cart_obj, new_obj
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def get_content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
    tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)
	# discounts
	# shipping

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-timestamp",]

    @property
    def is_digital(self):
        qs = CartItem.objects.filter(cart=self) #every product
        new_qs = qs.filter(product__is_digital=False) # every product that is not digial
        if new_qs.exists():
            return False
        return True

    def update_subtotal(self, instance):
        print("updating...")
        subtotal = 0
        items = CartItem.objects.filter(cart=instance)
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = "%.2f" %(subtotal)
        self.save()

    def is_complete(self):
        self.active = False
        self.save()

def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal:
        subtotal = Decimal(instance.subtotal)
        tax_total = round(subtotal * Decimal(instance.tax_percentage), 2) #8.5%
        total = round(subtotal + Decimal(tax_total), 2)
        instance.tax_total = "%.2f" %(tax_total)
        instance.total = "%.2f" %(total)
        instance.save()
    else:
        instance.total = 0.00
pre_save.connect(do_tax_and_total_receiver, sender=Cart)

# def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = CartItem.objects.filter(cart=instance)
#         total = 0
#         for x in products:
#             total += x.price
#         if instance.subtotal != total:
#             instance.subtotal = total
#             instance.save()
# m2m_changed.connect(m2m_changed_cart_receiver, sender=CartItem)
