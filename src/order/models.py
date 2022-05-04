from itertools import chain
import math
import datetime
from django.conf import settings
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse, get_object_or_404
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from src.address.models import Address
from src.billing.models import BillingProfile
from src.cart.models import Cart
from src.product.models import Product

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)

class OrderManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated", "-timestamp")

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        shipped = recent.not_refunded().by_status(status='shipped')
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data':recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7  # days_ago_start = 49
        days_ago_end = days_ago_start - (number_of_weeks * 7) #days_ago_end = 49 - 14 = 35
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end) 
        return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(updated__gte=start_date).filter(updated__lte=end_date)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated__day__gte=now.day)

    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))

    def cart_data(self):
        return self.aggregate(
            Sum("cart__products__price"),
            Avg("cart__products__price"),
            Count("cart__products")
        )

    def by_status(self, status="shipped"):
        return self.filter(status=status)

    def not_refunded(self):
        return self.exclude(status='refunded')

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')

class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, content_type, obj_id):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            content_type=content_type,
            object_id=obj_id,
            active=True,
            status='created'
        )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile,
                    content_type=content_type, object_id=obj_id)
            created = True
        return obj, created

    def filter_by_instance(self, request):
        qs = Package.objects.filter(admin=request.user)
        package = qs.first()
        content_cart = ContentType.objects.get(app_label='cart', model='cart')
        content_book = ContentType.objects.get(app_label='booking', model='booking')
        sale_orders = super(OrderManager, self).filter(
            content_type=content_cart).filter(package=package)
        booking_orders = super(OrderManager, self).filter(
            content_type=content_book).filter(package=package)
        queryset_chain = chain(
            booking_orders,
            sale_orders,
        )
        qs = sorted(
            queryset_chain,
            key=lambda instance: instance.pk,
            reverse=True
        )
        return qs

class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120, blank=True) # AB31DE3
    shipping_address = models.ForeignKey(Address, related_name="shipping_address", null=True, blank=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True, on_delete=models.CASCADE)
    shipping_address_final = models.TextField(blank=True, null=True)
    billing_address_final = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("order:detail", kwargs={'order_id': self.order_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded order"
        elif self.status == "shipped":
            return "Shipped"
        return "Shipping Soon"

    def update_total(self):
        content_cart = ContentType.objects.get(app_label='cart', model='cart')
        instance = get_object_or_404(Cart, id=self.object_id)
        new_total = math.fsum([instance.total, self.shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total = formatted_total
        self.save()
        return new_total

    def check_done(self):
        shipping_done = False
        content_cart = ContentType.objects.get(app_label='cart', model='cart')
        if self.content_type == content_cart:
            instance = Cart.objects.get_object_or_404(id=self.object_id)
            shipping_address_required = not instance.is_digital
            if shipping_address_required and self.shipping_address:
                shipping_done = True
            elif shipping_address_required and not self.shipping_address:
                shipping_done = False
            else:
                shipping_done = True
        else:
            shipping_done = True

        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_done and billing_address and total > 0:
            return True
        return False

    def update_purchases(self):
        content_cart = ContentType.objects.get(app_label='cart', model='cart')
        if self.content_type == content_cart:
            instance = Cart.objects.get_object_or_404(id=self.object_id)
            print(instance)
            print(self.object_id)
            for p in instance.products.all():
                obj, created = ProductPurchase.objects.get_or_create(
                    order_id=self.order_id,
                    product=p,
                    billing_profile=self.billing_profile
                )
        return ProductPurchase.objects.filter(order_id=self.order_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            if self.check_done():
                self.status = "paid"
                self.save()
                self.update_purchases()
        return self.status

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(content_type=instance.content_type, object_id=instance.object_id
        ).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)

    if instance.shipping_address and not instance.shipping_address_final:
        instance.shipping_address_final = instance.shipping_address.get_address()

    if instance.billing_address and not instance.billing_address_final:
        instance.billing_address_final = instance.billing_address.get_address()

pre_save.connect(pre_save_create_order_id, sender=Order)

# def post_save_cart_total(sender, instance, created, *args, **kwargs):
#     if not created:
#         cart_obj = instance
#         cart_total = cart_obj.total
#         cart_id = cart_obj.id
#         qs = Order.objects.filter(content_type='cart', object_id=cart_id)
#         if qs.count() == 1:
#             order_obj = qs.first()
#             order_obj.update_total()
# post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
post_save.connect(post_save_order, sender=Order)

class ProductPurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)

    def digital(self):
        return self.filter(product__is_digital=True)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

class ProductPurchaseManager(models.Manager):
    def get_queryset(self):
        return ProductPurchaseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def digital(self):
        return self.get_queryset().active().digital()

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def products_by_id(self, request):
        qs = self.by_request(request).digital()
        ids_ = [x.product.id for x in qs]
        return ids_

    def products_by_request(self, request):
        ids_ = self.products_by_id(request)
        products_qs = Product.objects.filter(id__in=ids_).distinct()
        return products_qs

class ProductPurchase(models.Model):
    order_id            = models.CharField(max_length=120)
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE) # billingprofile.productpurchase_set.all()
    product             = models.ForeignKey(Product, on_delete=models.CASCADE) # product.productpurchase_set.count()
    refunded            = models.BooleanField(default=False)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    objects = ProductPurchaseManager()

    def __str__(self):
        return self.product.title
