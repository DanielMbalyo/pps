from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    """ User-related CRUD form """
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Name'}
    ))
    address_line_1 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Address line 1'}
    ))
    address_line_2 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Address line 2'}
    ))
    city = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'City'}
    ))
    country = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Country'}
    ))
    state = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'State'}
    ))
    postal_code = forms.CharField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Postal Code'}
    ))

    class Meta:
        model = Address
        fields = [
            'name',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]
