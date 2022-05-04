from rest_framework import serializers
from src.shop.models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'name',
            'phone',
        ]