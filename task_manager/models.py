from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

def validate_password(value):
    if len(value) < 3:
        raise ValidationError(gettext_lazy('Your password must contain at least 3 characters.'))

def validate_passwords_match(password1, password2):
    if password1 != password2:
        raise ValidationError(gettext_lazy('Passwords do not match.'))


class CustomUser(AbstractUser):
    username_validator = RegexValidator(regex=r'^[\w.@+-]+$',message=gettext_lazy("Enter a valid username. Only letters, numbers, and the symbols @/./+/-/_ are allowed."))
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150,unique=True,validators=[username_validator])
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


class Status(models.Model):
    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    performer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks')
    labels = models.CharField(max_length=150)
    #labels = models.ManyToManyField(Label, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

