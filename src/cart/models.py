from decimal import Decimal
from django.conf import settings
from django.shortcuts import reverse, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete

from src.product.models import Product, UserProduct
from src.shop.models import Vendor

User = settings.AUTH_USER_MODEL

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(UserProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    product_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)

    def __str__(self):
        return self.product.product.title

def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    qty = instance.quantity
    if int(qty) >= 1:
        price = instance.product.sale_price
        instance.product_total = Decimal(qty) * Decimal(price)
pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.subtotal += instance.product_total
post_save.connect(cart_item_post_save_receiver, sender=CartItem)
# post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
    tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.vendor)

    class Meta:
        ordering = ["-timestamp",]

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

    def clear(self):
        self.subtotal = 0.00
        self.tax_total = 0.00
        self.total = 0.00
        self.save()

# def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
#     if instance.subtotal:
#         subtotal = Decimal(instance.subtotal)
#         tax_total = round(subtotal * Decimal(instance.tax_percentage), 2) #8.5%
#         total = round(subtotal + Decimal(tax_total), 2)
#         instance.tax_total = "%.2f" %(tax_total)
#         instance.total = "%.2f" %(total)
#         instance.save()
#     else:
#         instance.total = 0.00
# pre_save.connect(do_tax_and_total_receiver, sender=Cart)

def post_vendor_reciever(instance, created, *args, **kwargs):
    if created:
        Cart.objects.create(vendor=instance)
post_save.connect(post_vendor_reciever, sender=Vendor)
