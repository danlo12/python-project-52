from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

from .users.models import CustomUser

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': gettext_lazy('Username')}),
        label=gettext_lazy('Username')  # Перевод метки поля
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': gettext_lazy('Password')}),
        label=gettext_lazy('Password')  # Перевод метки поля
    )
