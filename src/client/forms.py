from django import forms
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

class ClientForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Name'}
    ))
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Username'}
    ))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Phone'}
    ))
    email = forms.CharField(required=True, label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Email'}
    ))
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Password'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Client.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists")
        return phone

    class Meta:
        model = Client
        fields = [
            "name",
            "username",
            "phone",
        ]
