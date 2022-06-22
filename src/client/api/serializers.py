import random
import string

from django.contrib.auth import get_user_model
from rest_framework import serializers
from src.account.api.serializers import UserSerializer
from src.client.models import Client, Finance

User = get_user_model()

class ClientSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = [
            "id", "first", "middle", "last", "gender", "dob", "citizenship", "region",
            "district", "street", "martial", "identification", "id_number", "phone"
        ]

class ClientCreateSerializer(serializers.Serializer):
    first = serializers.CharField(required=True, allow_blank=False, max_length=100)
    middle = serializers.CharField(required=True, allow_blank=False, max_length=100)
    last = serializers.CharField(required=True, allow_blank=False, max_length=100)
    gender = serializers.CharField(required=True, allow_blank=False, max_length=100)
    dob = serializers.CharField(required=True, allow_blank=False, max_length=100)
    citizenship = serializers.CharField(required=True, allow_blank=False, max_length=100)
    region = serializers.CharField(required=True, allow_blank=False, max_length=100)
    district = serializers.CharField(required=True, allow_blank=False, max_length=100)
    street = serializers.CharField(required=True, allow_blank=False, max_length=100)
    martial = serializers.CharField(required=True, allow_blank=False, max_length=100)
    identification = serializers.CharField(required=True, allow_blank=False, max_length=100)
    id_number = serializers.CharField(required=True, allow_blank=False, max_length=100)
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
        user_qs = Client.objects.filter(phone=data.get("phone")).first()
        if user_qs is not None:
            raise serializers.ValidationError("This Phone Number has already registered.")
        return value

    def create(self, validated_data):
        password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(15))
        account = User.objects.create_user(email=validated_data['email'], password=password)
        client = Client.objects.create(
            account=account, first=validated_data['first'], middle=validated_data["middle"], last=validated_data["last"], 
            gender=validated_data["gender"], dob=validated_data["dob"], citizenship=validated_data["citizenship"], 
            region=validated_data["region"], district=validated_data["district"], street=validated_data["street"], 
            martial=validated_data["martial"], identification=validated_data["identification"], id_number=validated_data["id_number"], 
            phone=validated_data['phone'],)
        validated_data['id'] = client.id
        return validated_data

class ClientFinanceSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, allow_blank=False, max_length=100)
    source = serializers.CharField(required=True, allow_blank=False, max_length=100)
    employer = serializers.CharField(required=True, allow_blank=False, max_length=100)
    referee = serializers.CharField(required=True, allow_blank=False, max_length=100)
    branch = serializers.CharField(required=True, allow_blank=False, max_length=100)
    duration = serializers.CharField(required=True, allow_blank=False, max_length=100)
    range = serializers.CharField(required=True, allow_blank=False, max_length=100)
    dependants = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def create(self, validated_data):
        client = Client.objects.filter(id=validated_data['id']).first()
        Finance.objects.create(
            client=client, source=validated_data['source'], employer=validated_data["employer"], 
            referee=validated_data["referee"], branch=validated_data["branch"], duration=validated_data["duration"], 
            range=validated_data["range"], dependants=validated_data["dependants"],
        )
        return validated_data