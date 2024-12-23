from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy

class CustomUser(AbstractUser):
    username_validator = RegexValidator(regex=r'^[\w.@+-]+$',message=gettext_lazy("Enter a valid username. Only letters, numbers, and the symbols @/./+/-/_ are allowed."))
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150,unique=True,validators=[username_validator])
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
