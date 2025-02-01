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
from .models import Label


logger = logging.getLogger(__name__)

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

    def form_valid(self, form):
        name = form.cleaned_data['name']
        if Label.objects.filter(name=name).exists():
            messages.error(self.request, gettext_lazy('Label with this name already exists.'))
            return redirect('label_create')
        messages.success(self.request, gettext_lazy('Label successfully create'))
        return super().form_valid(form)


class LabelsUpdateView(UpdateView):
    model = Label
    template_name = 'label_update.html'
    fields = ['name']
    success_url = reverse_lazy('labels')
    context_object_name = "label"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        if request.method == "POST":
            messages.success(request, gettext_lazy('Label successfully update'))
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
        if request.method == "POST":
            if label.task_set.exists():
                messages.error(request, gettext_lazy('Cannot delete label because it is associated with tasks.'))
                return redirect('labels')
            messages.success(request, gettext_lazy('Label successfully delete'))
        return super().dispatch(request, *args, **kwargs)
