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
        if request.method == "POST":
            messages.success(request, gettext_lazy('Status successfully create'))
        return super().dispatch(request, *args, **kwargs)


class StatusesUpdateView(UpdateView):
    model = Status
    template_name = 'status_update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses')
    context_object_name = "status"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        if request.method == "POST":
            messages.success(request, gettext_lazy('Status successfully update'))
        return super().dispatch(request, *args, **kwargs)

class StatusesDeleteView(DeleteView):
    model = Status
    template_name = 'status_delete.html'
    success_url = reverse_lazy('statuses')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('Cannot delete status'))
            return redirect('login')
        if request.method == "POST":
            messages.success(request, gettext_lazy('Status successfully deleted'))
        return super().dispatch(request, *args, **kwargs)