from rest_framework import serializers
from src.shop.models import Shop, Vendor
import random
import string

from django.contrib.auth import get_user_model
from src.account.api.serializers import UserSerializer

User = get_user_model()

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id", "name", "category", "tin_number", "contacts", "region",
            "district", "street", "lon", "lat", "opening", "closing", "description",
        ]

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "id", "first", "middle", "last", "gender", "dob",
            "citizenship", "region", "district", "street", "phone",
        ]

class ShopCreateSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, allow_blank=False, max_length=100)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    category = serializers.CharField(required=True, allow_blank=False, max_length=100)
    tin_number = serializers.CharField(required=True, allow_blank=False, max_length=100)
    contacts = serializers.CharField(required=True, allow_blank=False, max_length=100)
    region = serializers.CharField(required=True, allow_blank=False, max_length=100)
    district = serializers.CharField(required=True, allow_blank=False, max_length=100)
    street = serializers.CharField(required=True, allow_blank=False, max_length=100)
    lon = serializers.CharField(required=True, allow_blank=False, max_length=100)
    lat = serializers.CharField(required=True, allow_blank=False, max_length=100)
    opening = serializers.CharField(required=True, allow_blank=False, max_length=100)
    closing = serializers.CharField(required=True, allow_blank=False, max_length=100)
    description = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def create(self, validated_data):
        vendor = Vendor.objects.filter(id=validated_data['id']).first()
        Shop.objects.create(
            owner=vendor, name=validated_data['name'], category=validated_data["category"], tin_number=validated_data["tin_number"],
            region=validated_data["region"], contacts=validated_data["contacts"], district=validated_data["district"], 
            street=validated_data["street"], lon=validated_data["lon"], lat=validated_data["lat"],
            opening=validated_data["opening"], closing=validated_data["closing"], description=validated_data["description"],
        )
        return validated_data

class VendorCreateSerializer(serializers.Serializer):
    first = serializers.CharField(required=True, allow_blank=False, max_length=100)
    middle = serializers.CharField(required=True, allow_blank=False, max_length=100)
    last = serializers.CharField(required=True, allow_blank=False, max_length=100)
    gender = serializers.CharField(required=True, allow_blank=False, max_length=100)
    dob = serializers.CharField(required=True, allow_blank=False, max_length=100)
    citizenship = serializers.CharField(required=True, allow_blank=False, max_length=100)
    region = serializers.CharField(required=True, allow_blank=False, max_length=100)
    district = serializers.CharField(required=True, allow_blank=False, max_length=100)
    street = serializers.CharField(required=True, allow_blank=False, max_length=100)
    phone = serializers.CharField(required=True, allow_blank=False, max_length=100)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        data = self.get_initial()
        user_qs = User.objects.filter(email=data.get("email")).first()
        if user_qs is not None:
            raise serializers.ValidationError("This Email has already registered.")
        return value

    def validate_phone(self, value):
        data = self.get_initial()
        user_qs = Vendor.objects.filter(phone=data.get("phone")).first()
        if user_qs is not None:
            raise serializers.ValidationError("This Phone Number has already registered.")
        return value

    def create(self, validated_data):
        password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
        account = User.objects.create_user(email=validated_data['email'], password=password)
        vendor = Vendor.objects.create(
            account=account, first=validated_data['first'], middle=validated_data["middle"], last=validated_data["last"], 
            gender=validated_data["gender"], dob=validated_data["dob"], citizenship=validated_data["citizenship"], 
            region=validated_data["region"], district=validated_data["district"], street=validated_data["street"], 
            phone=validated_data['phone'],)
        validated_data['id'] = vendor.id
        return validated_data
    