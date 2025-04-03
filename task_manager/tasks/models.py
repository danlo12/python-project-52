from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    performer = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(CustomUser,
                                on_delete=models.CASCADE,
                                related_name='created_tasks')
    labels = models.ManyToManyField(Label, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
