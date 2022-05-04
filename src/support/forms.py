from django import forms
from .models import NewsLetter, Contact

class SubscriptionForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email?', required=False)
    class Meta:
        model = NewsLetter
        fields = [
            'subscribed'
        ]

class NewsLetterForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={
            "class": "form-control", "placeholder": "Your email"
        })
    )
    class Meta:
        model = NewsLetter
        fields = [
            'email'
        ]

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label='Name', widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "Your full name"
        })
    )
    email = forms.EmailField(
        label='Email', widget=forms.EmailInput(attrs={
            "class": "form-control", "placeholder": "Your email"
        })
    )
    phone = forms.CharField(
        label='Phone', widget=forms.TextInput(attrs={
            "class": "form-control", "placeholder": "Your phone"
        })
    )
    subject = forms.CharField(
        label='Subject', widget=forms.TextInput(attrs={
            'class': 'form-control', "placeholder": "Your subject"
        })
    )
    content = forms.CharField(
        label='Message', widget=forms.Textarea(attrs={
            'class': 'form-control', "placeholder": "Your message"
        })
    )

    class Meta:
        model = Contact
        fields = [
            'name', 'email', 'subject', 'phone', 'content'
        ]

class SingleMailForm(forms.Form):
    sender = forms.CharField(
        label='Sender', widget=forms.TextInput(attrs={
            'class': 'form-control', "placeholder": "Sender"
        })
    )
    recipient = forms.CharField(
        label='Recipient', widget=forms.TextInput(attrs={
            'class': 'form-control', "placeholder": "Recipient"
        })
    )
    cc_myself = forms.CharField(
        label='Cc', widget=forms.TextInput(attrs={
            'class': 'form-control', "placeholder": "Carbon copy"
        })
    )
    subject = forms.CharField(
        label='Subject', widget=forms.TextInput(attrs={
            'class': 'form-control', "placeholder": "Subject"
        })
    )
    message = forms.CharField(
        label='Message', widget=forms.Textarea(attrs={
            'class': 'form-control', "placeholder": "Your message"
        })
    )
