from django import forms
from .models import Shop, Vendor

class VendorForm(forms.ModelForm):
    first = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'First Name'}
    ))
    middle = forms.CharField(label='Middle Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Middle Name'}
    ))
    last = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Last Name'}
    ))
    # phone = forms.CharField(label='Phone', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Phone'}
    # ))
    # location = forms.CharField(label='Location', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Location'}
    # ))
    # lon = forms.CharField(label='Longitude', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Longitude'}
    # ))
    # lat = forms.CharField(label='Latitude', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Latitude'}
    # ))
    # opening = forms.CharField(label='Opening', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Opening'}
    # ))
    # closing = forms.CharField(label='Closing', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Closing'}
    # ))
    # description = forms.CharField(label='Description', widget=forms.Textarea(
    #     attrs={'class': 'form-control', 'placeholder': 'Description'}
    # ))

    class Meta:
        model = Vendor
        fields = [
            "first",
            "middle",
            "last",
            "gender",
            "dob",
            "citizenship",
            "location",
            "phone",
        ]

class ShopForm(forms.ModelForm):
    # name = forms.CharField(label='Name', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Name'}
    # ))
    # phone = forms.CharField(label='Phone', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Phone'}
    # ))
    # location = forms.CharField(label='Location', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Location'}
    # ))
    # lon = forms.CharField(label='Longitude', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Longitude'}
    # ))
    # lat = forms.CharField(label='Latitude', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Latitude'}
    # ))
    # opening = forms.CharField(label='Opening', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Opening'}
    # ))
    # closing = forms.CharField(label='Closing', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Closing'}
    # ))
    # description = forms.CharField(label='Description', widget=forms.Textarea(
    #     attrs={'class': 'form-control', 'placeholder': 'Description'}
    # ))

    class Meta:
        model = Shop
        fields = [
            "name",
            "category", 
            "tin_number",
            "contacts",
            "region",
            "district",
            "lon",
            "lat",
            "opening",
            "closing",
            "description",
        ]
