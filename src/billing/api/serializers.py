from rest_framework import serializers

from src.order.models import Order, ProductPurchase
from src.billing.models import BillingProfile, Charge
from src.product.api.serializers import UserProductListSerializer

class BillingSerializer(serializers.ModelSerializer):

	class Meta:
		model = BillingProfile
		fields = [
			"amount", "expected", "active", "update",
		]

class ChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Charge
		fields = [
			"paid", "refunded", "amount",
			"currency", "date",
		]
