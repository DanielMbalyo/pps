from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError
)

User = get_user_model()

class DetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

class CreateSerializer(ModelSerializer):
    email = EmailField(label='Email')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'password',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email = data.get("email")
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        phone = validated_data['phone']
        password = validated_data['password']
        user_obj = User(email = email, phone = phone,)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
