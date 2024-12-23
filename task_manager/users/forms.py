from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from .models import CustomUser


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

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_check = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check')

        if password and password != password_check:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
