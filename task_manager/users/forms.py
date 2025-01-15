from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        return cleaned_data
