from rest_framework import serializers
from src.support.models import Contact, NewsLetter

class NewsletterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = [
            'email',
        ]

class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'phone',
            'content'
        ]
