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

class CheckoutSerializer(TokenMixin, serializers.Serializer):
    nickname = serializers.CharField()
    name = serializers.CharField()
    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField(required=False)
    city = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    postal_code = serializers.IntegerField()
    address_id = serializers.IntegerField(required=False)
    billing_id = serializers.CharField()

    def validate(self, data):
        nickname = data.get("nickname")
        name = data.get("name")
        address_line_1 = data.get("address_line_1")
        address_line_2 = data.get("address_line_2")
        city = data.get("city")
        country = data.get("country")
        state = data.get("state")
        postal_code = data.get("postal_code")
        billing_profile = BillingProfile.objects.get(customer_id=str(data.get("billing_id")))

        try:
            address_obj, address_obj_created = Address.objects.get_or_create(
                nickname=nickname, name=name, billing_profile=billing_profile,
                address_line_1=address_line_1, address_line_2=address_line_2,
                city=city, country=country, state=state, postal_code=postal_code
            )
            data['address_id'] = address_obj.id
        except:
            raise serializers.ValidationError("This is not a valid address for this user")
        return data

class FinalizedCheckoutSerializer(TokenMixin, serializers.Serializer):
    order_token = serializers.CharField()
    payment_method_nonce = serializers.CharField()
    order_id =  serializers.IntegerField(required=False)
    user_checkout_id = serializers.IntegerField(required=False)

    def validate(self, data):
        order_token = data.get("order_token")
        order_data = self.parse_token(order_token)
        order_id = order_data.get("order_id")
        user_checkout_id = order_data.get("user_checkout_id")

        try:
            data["order_id"] = order_id
            data["user_checkout_id"] = user_checkout_id
        except:
            raise serializers.ValidationError("This is not a valid order for this user.")

        payment_method_nonce = data.get("payment_method_nonce")
        if payment_method_nonce == None:
            raise serializers.ValidationError("This is not a valid payment method nonce")
        return data
