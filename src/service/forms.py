from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Name'}
    ))
    number = forms.CharField(label='Number', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Number'}
    ))
    image = forms.ImageField(label='Image',)

    class Meta:
        model = Service
        fields = [
            "name",
            "number",
            "image",
        ]
