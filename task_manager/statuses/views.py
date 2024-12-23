from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import logging

from task_manager.filters import TaskFilter
from .models import Status
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


logger = logging.getLogger(__name__)
class StatusesListView(ListView):
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class StatusesCreateView(CreateView):
    model = Status
    template_name = 'status_create.html'
    fields = ['name']
    context_object_name = 'statuses'
    success_url = reverse_lazy('statuses')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class StatusesUpdateView(UpdateView):
    model = Status
    template_name = 'status_update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class StatusesDeleteView(DeleteView):
    model = Status
    template_name = 'status_delete.html'
    success_url = reverse_lazy('statuses')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['pk'])

        if task.creator.id != request.user.id:
            messages.error(request, gettext_lazy('You do not have permission to edit this task.'))
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_card.html'
    context_object_name = 'task'

class LabelsListView(ListView):
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class LabelsCreateView(CreateView):
    model = Label
    template_name = 'label_create.html'
    fields = ['name']
    context_object_name = 'labels'
    success_url = reverse_lazy('labels')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class LabelsUpdateView(UpdateView):
    model = Label
    template_name = 'label_update.html'
    fields = ['name']
    success_url = reverse_lazy('labels')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class LabelsDeleteView(DeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('labels')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        label = self.get_object()
        if label.task_set.exists():
            messages.error(request, gettext_lazy('Cannot delete label because it is associated with tasks.'))
            return redirect('labels')
        return super().dispatch(request, *args, **kwargs)
