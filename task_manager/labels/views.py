import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Label

logger = logging.getLogger(__name__)


class LabelsListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()


class LabelsCreateView(LoginRequiredMixin, CreateView):
    model = Label
    template_name = 'label_create.html'
    fields = ['name']
    context_object_name = 'labels'
    success_url = reverse_lazy('labels')
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def form_valid(self, form):
        name = form.cleaned_data['name']
        if Label.objects.filter(name=name).exists():
            messages.error(self.request, gettext_lazy(
                'Label with this name already exists.'))
            return redirect('label_create')
        messages.success(self.request, gettext_lazy(
            'Label successfully create'))
        return super().form_valid(form)


class LabelsUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    template_name = 'label_update.html'
    fields = ['name']
    success_url = reverse_lazy('labels')
    context_object_name = "label"
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        label = self.get_object()
        if request.method == "POST":
            if label.task_set.exists():
                messages.error(request, gettext_lazy(
                    'Cannot delete label because it is associated with tasks.'))
                return redirect('labels')
            messages.success(request, gettext_lazy('Label successfully delete'))
        return super().dispatch(request, *args, **kwargs)



class LabelsDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('labels')
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        label = self.get_object()
        if request.method == "POST":
            if label.task_set.exists():
                messages.error(request, gettext_lazy(
                    'Cannot delete label because it is associated with tasks.'))
                return redirect('labels')
            messages.success(request, gettext_lazy('Label successfully delete'))
        return super().dispatch(request, *args, **kwargs)
