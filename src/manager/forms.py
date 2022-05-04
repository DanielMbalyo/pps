from django import forms

from .models import Manager

class ManagerForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Email'}
    ))
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Name'}
    ))
    phone = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Phone'}
    ))
    # profile = forms.ImageField(label='Profile', )

    class Meta:
        model = Manager
        fields = ["name", "phone",] # "profile",]