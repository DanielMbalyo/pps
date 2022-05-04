import random
import string

from django.contrib.auth import get_user_model
from rest_framework import serializers
from src.account.api.serializers import UserSerializer
from src.client.models import Client

User = get_user_model()

client_url = serializers.HyperlinkedIdentityField(
    view_name='client_api:detail', lookup_field='slug' )

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = [
            'user',
            'name',
            'slug',
            'phone',
        ]

class ClientCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    phone = serializers.CharField(required=True, allow_blank=False, max_length=100)
    email = serializers.EmailField(required=True)
    staff = serializers.BooleanField(required=False)

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
        # if validated_data['staff']:
        Client.objects.create(account=account, name=validated_data['name'], phone=validated_data['phone'],)
        return validated_data
        # else:
        #     return Manager.objects.create(account=account, name=validated_data['name'], phone=validated_data['phone'],)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
   