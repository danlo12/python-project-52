from django import forms
from .models import CustomUser
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','password','password_check']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if password != password_check:
            raise ValidationError(gettext_lazy("Passwords do not match."))

        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))