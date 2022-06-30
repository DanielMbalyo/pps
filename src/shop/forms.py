import datetime
from django import forms
from .models import Shop, Vendor, GENDER, CATEGORIES, PAYMENT

class InquiryForm(forms.Form):
    inqury = forms.CharField(label='Reply', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Reply'}
    ), help_text='class')

class VendorForm(forms.ModelForm):
    first = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'First Name'}
    ), help_text='class')
    middle = forms.CharField(label='Middle Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Middle Name'}
    ), help_text='class', required=False)
    last = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Last Name'}
    ), help_text='class')
    phone = forms.CharField(label='Phone', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Phone'}
    ), help_text='class')
    region = forms.CharField(label='Region', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Region'}
    ), help_text='class')
    district = forms.CharField(label='District', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'District'}
    ), help_text='class')
    street = forms.CharField(label='Street', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Street'}
    ), help_text='class')
    citizenship = forms.CharField(label='Citizenshp', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Citizenshp'}
    ), help_text='class', initial='Tanzanian')
    dob = forms.CharField(label='Birth Date', widget=forms.DateInput(
        attrs={'class': 'form-contol', 'type': 'date', 'placeholder':''}
    ), help_text='class', initial=datetime.date.today)
    gender = forms.ChoiceField(label='Gender', choices=GENDER, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      help_text='class')
    means = forms.ChoiceField(label='Payment Means', choices=PAYMENT, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      help_text='class')
    number = forms.CharField(label='Payment Number', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Payment Number'}
    ), help_text='class')

    class Meta:
        model = Vendor
        fields = [
            "first",
            "middle",
            "last",
            "gender",
            "dob",
            "citizenship",
            "region",
            "district",
            "street",
            "phone",
            "means",
            "number",
        ]

class ShopForm(forms.ModelForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Name'}
    ), help_text='class')
    contacts = forms.CharField(label='Contacts', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Contacts'}
    ), help_text='class')
    region = forms.CharField(label='Region', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Region'}
    ), help_text='class')
    district = forms.CharField(label='District', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'District'}
    ), help_text='class')
    street = forms.CharField(label='Street', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Street'}
    ), help_text='class')
    tin_number = forms.CharField(label='Tin Number', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Tin Number'}
    ), help_text='class')
    # lon = forms.CharField(label='Longitude', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Longitude'}
    # ), help_text='class')
    # lat = forms.CharField(label='Latitude', widget=forms.TextInput(
    #     attrs={'class': 'form-control', 'placeholder':'Latitude'}
    # ), help_text='class')
    opening = forms.CharField(label='Opening', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Opening'}
    ), help_text='class')
    closing = forms.CharField(label='Closing', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Closing'}
    ), help_text='class')
    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Description'}
    ), help_text='class')
    category = forms.ChoiceField(label='Type', choices=CATEGORIES, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      help_text='class')

    class Meta:
        model = Shop
        fields = [
            "name",
            "category", 
            "tin_number",
            "contacts",
            "region",
            "district",
            "street",
            "opening",
            "closing",
            "description",
        ]

class LocationForm(forms.ModelForm):
    lon = forms.CharField(label='Longitude', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Longitude'}
    ), help_text='class')
    lat = forms.CharField(label='Latitude', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Latitude'}
    ), help_text='class')

    class Meta:
        model = Shop
        fields = [
            "lat",
            "lon", 
        ]
