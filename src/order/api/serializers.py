from rest_framework import serializers

from src.order.models import Order

class OrderDetailSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="order_api:detail")
	# subtotal = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = [
			"url",
			"order_id",
			# "user",
			"shipping_address",
			"billing_address",
			# "shipping_total_price",
			# "subtotal",
			"total",
		]

	def get_subtotal(self, obj):
		return obj.cart.subtotal

class OrderSerializer(serializers.ModelSerializer):
	# subtotal = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = [
			"id",
			# "user",
			"shipping_address",
			"billing_address",
			# "shipping_total_price",
			# "subtotal",
			"total",
		]

	def get_subtotal(self, obj):
		return obj.cart.subtotal

