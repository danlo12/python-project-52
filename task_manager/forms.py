from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': gettext_lazy('Username'),'label':"1"}),
        label=gettext_lazy('Username')  # Перевод метки поля
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': gettext_lazy('Password')}),
        label=gettext_lazy('Password')  # Перевод метки поля
    )
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)
        for field in self.fields.values():
            field.label = field.label.rstrip("")
