import datetime
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.shortcuts import reverse
from decimal import Decimal 
from src.client.models import Client
from src.shop.models import Vendor
from src.order.models import Order

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        pass

class BillingProfile(models.Model):
    client = models.OneToOneField(Client, null=True, blank=True, on_delete=models.CASCADE)
    vendor = models.OneToOneField(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    expected = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

    def charge(self, order_obj, card=None):
        return Charge.objects.do(self, order_obj)

class ChargeManager(models.Manager):
    def do(self, billing, order_obj, card=None): # Charge.objects.do()
        card_obj = card
        if card_obj is None:
            cards = billing.card_set.filter(default=True) # card_obj.billing_profile
            if cards.exists():
                card_obj = cards.first()
        if card_obj is None:
            return False, "No cards available"
        c = stripe.Charge.create(
              amount = int(float(order_obj.total) * 100), # 39.19 --> 3919
              currency = "usd",
              customer =  billing_profile.customer_id,
              source = card_obj.stripe_id,
              metadata={"order_id":order_obj.order_id},
            )
        new_charge_obj = self.model(
                billing = billing,
                paid = c.paid,
                refunded = c.refunded,
                outcome = c.outcome,
                outcome_type = c.outcome['type'],
                seller_message = c.outcome.get('seller_message'),
                risk_level = c.outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.seller_message 

class Charge(models.Model):
    billing = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    amount = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    currency = models.CharField(max_length=120, default="TZS",)
    date = models.DateField(default=datetime.date.today)

    objects = ChargeManager()
