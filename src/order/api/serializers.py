from rest_framework import serializers

from src.order.models import Order, ProductPurchase
from src.product.api.serializers import UserProductListSerializer

class PurchaseSerializer(serializers.ModelSerializer):
	product = UserProductListSerializer(read_only=True)
	class Meta:
		model = ProductPurchase
		fields = [
			"product", "quantity", "amount",  
    		"refunded", "updated",
		]

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = [
			"order_id", "vendor", "client",
			"complete", "active", "total",
		]
