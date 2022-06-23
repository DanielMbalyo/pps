from rest_framework import serializers

from src.cart.models import CartItem
from .mixins import TokenMixin

class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = [
            "title",
            "price",
            "product",
            "quantity",
            "product_total",
        ]

    def get_title(self, obj):
        return "%s" %(obj.product)

    def get_product(self, obj):
        return obj.product.id

    def get_price(self, obj):
        return obj.product.sale_price
