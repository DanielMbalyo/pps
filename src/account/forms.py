from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)

User = get_user_model()

CATEGORIES = (
    ('client', 'Client Account'),
    ('shop', 'Vendor Account'),
)

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password',)

    def clean_password(self):
        return self.initial["password"]

class RegistrationForm(forms.Form):
    email = forms.CharField(required=True, label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Email'}
    ))
    type = forms.ChoiceField(label='Account Type',
        choices=CATEGORIES, required=True,  widget=forms.Select(attrs={'class': 'form-control'}),)
    
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Email already exists")
    #     return email

class LoginForm(forms.Form):
    """A form for login users. Includes all the required
    fields, plus a remember me field."""
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Email'}
        ))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Password'}
    ))
    remember_me = forms.BooleanField(label='Remember Me', widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input', 'placeholder':''}
    ), required=False)

    def __init__(self, *args, request=None, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

class ActivateForm(forms.Form):
    email = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'New Password'}
    ))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Confirm New Password'}
    ))

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

class UserForm(forms.ModelForm):
    """A form for updating user details. Includes all the required
    fields."""
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Email'}
    ))

    class Meta:
        model = User
        fields = ('email', )

    def clean_email(self):
        # checks if an email is taken
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

class ChangePassForm(PasswordChangeForm):
    """A form for changing password for users. Includes all the required
    fields, plus a repeated password."""
    old_password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Old Password'}
    ))
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'New Password'}
    ))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Confirm New Password'}
    ))

class ResetPassForm(PasswordResetForm):
    """A form for submiting an email when a user fogets it."""
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Email'}
    ))

class SetPassForm(SetPasswordForm):
    """A form for changing passwords without putting in an old password."""
    new_password1 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'New Password'}
    ))
    new_password2 = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder':'Confirm New Password'}
    ))
