from rest_framework import serializers
from src.account.api.serializers import UserSerializer
from src.product.models import Product, UserProduct
from src.shop.models import Shop, Vendor

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'active',
            'image',
        ]

class UserProductListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    class Meta:
        model = UserProduct
        fields = [
            'id',
            'description',
            'sale_price',
            'quantity',
            'active',
            'product',
        ]

class ProductCreateSerializer(serializers.Serializer):
    product = serializers.CharField(required=True, allow_blank=False, max_length=100)
    vendor = serializers.CharField(required=True, allow_blank=False, max_length=100)
    description = serializers.CharField(required=True, allow_blank=False, max_length=100)
    sale_price = serializers.CharField(required=True, allow_blank=False, max_length=100)
    quantity = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def create(self, validated_data):
        product = Product.objects.filter(id=validated_data['product']).first()
        vendor = Vendor.objects.filter(id=validated_data['vendor']).first()
        UserProduct.objects.create(
            product=product, vendor=vendor, description=validated_data['description'],
            sale_price=validated_data["sale_price"], quantity=validated_data["quantity"], active=True,
        )
        return validated_data

