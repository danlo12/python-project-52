from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser
from task_manager.labels.models import Label

class Task(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    performer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks')
    labels = models.ManyToManyField(Label, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

