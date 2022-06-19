import datetime
from django import forms
from django.contrib.auth import get_user_model
from .models import (
    Client, Finance, GENDER, MARTIAL, IDS, SOURCE, RANGE, STATUS, DURATION
)

User = get_user_model()

class InquiryForm(forms.Form):
    inqury = forms.CharField(label='Reply', widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Reply'}
    ), help_text='class')

class ClientForm(forms.ModelForm):
    first = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'First Name',}
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
    id_number = forms.CharField(label='ID Number', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'ID Number'}
    ), help_text='class')
    dob = forms.CharField(label='Birth Date', widget=forms.DateInput(
        attrs={'class': 'form-contol', 'type': 'date', 'placeholder':''}
    ), help_text='class', initial=datetime.date.today)
    gender = forms.ChoiceField(label='Gender', choices=GENDER, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      help_text='class')
    martial = forms.ChoiceField(label='Martial Status', choices=MARTIAL, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='class')
    identification = forms.ChoiceField(label='ID Type', choices=IDS, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='class')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Client.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists")
        return phone

    class Meta:
        model = Client
        fields = [
            "first", "middle", "last", "gender", "dob", "citizenship",
            "region",
            "district",
            "street", "martial", "identification", "id_number", "phone"
        ]


class FinanceForm(forms.ModelForm):
    status = forms.ChoiceField(label='Status', choices=STATUS, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
     help_text='class')
    source = forms.ChoiceField(label='Source', choices=SOURCE, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
     help_text='class')
    employer = forms.CharField(label='Company/Employer Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Company/Employer Name'}
    ), help_text='class')
    position = forms.CharField(label='Employement Position', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Employement Position'}
    ), help_text='class')
    referee = forms.CharField(label='Referee Phone', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Referee Phone'}
    ), help_text='class')
    branch = forms.CharField(label='Business/Office Location', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Business/Office Location'}
    ), help_text='class')
    duration = forms.ChoiceField(label='Duration', choices=DURATION, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}), 
      help_text='class')
    range = forms.ChoiceField(label='Range', choices=RANGE, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}), 
      help_text='class')
    dependants = forms.ChoiceField(label='No Of Dependants', choices=RANGE, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}), 
      help_text='class')

    class Meta:
        model = Finance
        fields = [
            "source", "employer", "referee", "branch", 
            "duration", "range", "dependants", 
        ]