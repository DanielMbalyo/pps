from django import forms

from .models import Product, UserProduct

class ProductForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':''}
    ))
    image = forms.ImageField(label='Image',)
    price = forms.DecimalField(label='Price', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':''}
    ))
    active = forms.BooleanField(label='Active', widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder':''}
    ), required=False)

    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'image',
            'active',
        ]

class UserProductForm(forms.ModelForm):
    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder':''}
    ))
    sale_price = forms.DecimalField(label='Price', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':''}
    ))
    quantity = forms.DecimalField(label='Quantity', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':''}
    ))
    active = forms.BooleanField(label='Active', widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder':''}
    ), required=False)

    class Meta:
        model = UserProduct
        fields = [
            'description',
            'sale_price',
            'active',
        ]

