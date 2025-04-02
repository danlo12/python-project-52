import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Status

logger = logging.getLogger(__name__)


class StatusesListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()


class StatusesCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'status_create.html'
    fields = ['name']
    context_object_name = 'statuses'
    success_url = reverse_lazy('statuses')
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.success(request,
                             gettext_lazy('Status successfully create'))
        return super().dispatch(request, *args, **kwargs)


class StatusesUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'status_update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses')
    context_object_name = "status"
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.success(request,
                             gettext_lazy('Status successfully update'))
        return super().dispatch(request, *args, **kwargs)


class StatusesDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'status_delete.html'
    success_url = reverse_lazy('statuses')
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.method == "POST":
            if self.object.task_set.exists():
                messages.error(request, gettext_lazy('Cannot delete status'))
                return redirect('statuses')
            messages.success(request,
                             gettext_lazy('Status successfully deleted'))
        return super().dispatch(request, *args, **kwargs)
