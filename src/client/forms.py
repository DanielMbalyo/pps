from django import forms
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

class ClientForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Name'}
    ))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Phone'}
    ))
    employer = forms.CharField(label='Employer', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Company Name'}
    ))
    branch = forms.CharField(label='Branch', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Branch Name'}
    ))
    office_phone = forms.CharField(label='Employer Contact', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Employer Contact'}
    ))
    months = forms.CharField(label='Duration', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Employment Duration'}
    ))
    nid = forms.CharField(label='NID', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'National ID'}
    ))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Client.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists")
        return phone

    class Meta:
        model = Client
        fields = [
            "name", "phone", "employer",
            "branch", "office_phone", "months", "nid" 
        ]
