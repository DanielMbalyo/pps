from rest_framework import serializers

from src.order.models import Order, ProductPurchase
from src.billing.models import BillingProfile, Charge
from src.product.api.serializers import UserProductListSerializer

class BillingSerializer(serializers.ModelSerializer):

	class Meta:
		model = BillingProfile
		fields = [
			"product", "quantity", "amount", "refunded",
		]

class ChargeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Charge
		fields = [
			"order_id", "vendor", "client",
			"complete", "active", "total",
		]
