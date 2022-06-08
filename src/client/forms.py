import datetime
from django import forms
from django.contrib.auth import get_user_model
from .models import Client, Finance, GENDER, MARTIAL, IDS, SOURCE

User = get_user_model()

class ClientForm(forms.ModelForm):
    first = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'First Name'}
    ))
    middle = forms.CharField(label='Middle Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Middle Name'}
    ), required=False)
    last = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Last Name'}
    ))
    phone = forms.CharField(label='Phone', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Phone'}
    ))
    location = forms.CharField(label='Location', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Current Residence'}
    ))
    citizenship = forms.CharField(label='Citizenshp', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Citizenshp'}
    ), initial='Tanzanian')
    id_number = forms.CharField(label='ID Number', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'ID Number'}
    ))
    dob = forms.CharField(label='Birth Date', widget=forms.DateInput(
        attrs={'class': 'form-contol', 'type': 'date', 'placeholder':''}
    ), initial=datetime.date.today)
    gender = forms.ChoiceField(label='Gender', choices=GENDER, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),)
    martial = forms.ChoiceField(label='Martial Status', choices=MARTIAL, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),)
    identification = forms.ChoiceField(label='ID Type', choices=IDS, required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Client.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Phone already exists")
        return phone

    class Meta:
        model = Client
        fields = [
            "first", "middle", "last", "gender", "dob", "citizenship",
            "location", "martial", "identification", "id_number", "phone"
        ]


class FinanceForm(forms.ModelForm):
    source = forms.ChoiceField(label='Source', choices=SOURCE, required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),)
    employer = forms.CharField(label='Company/Employer Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Company/Employer Name'}
    ))
    referee = forms.CharField(label='Referee Phone', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Referee Phone'}
    ))
    branch = forms.CharField(label='Business/Office Location', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Business/Office Location'}
    ))
    duration = forms.CharField(label='Employment/Business Duration', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Employment/Business Duration'}
    ))
    range = forms.CharField(label='Monthly Income', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Monthly Income'}
    ))
    dependants = forms.CharField(label='No Of Dependants', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'No Of Dependants'}
    ))

    class Meta:
        model = Finance
        fields = [
            "source", "employer", "referee", "branch", 
            "duration", "range", "dependants", 
        ]