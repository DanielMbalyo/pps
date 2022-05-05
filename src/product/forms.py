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
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Product',
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Product'}),)
    description = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder':'Description'}
    ))
    sale_price = forms.DecimalField(label='Price', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Price'}
    ))
    quantity = forms.DecimalField(label='Quantity', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Quantity'}
    ))
    active = forms.BooleanField(label='Active', widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder':'Active'}
    ), required=False)

    class Meta:
        model = UserProduct
        fields = [
            'product',
            'description',
            'sale_price',
            'quantity',
            'active',
        ]

