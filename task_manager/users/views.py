from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import logging

from task_manager.filters import TaskFilter
from .forms import UserRegistrationForm, UserUpdateForm
from .models import CustomUser


logger = logging.getLogger(__name__)

class UserPermissionMixin:
    def check_user_permission(self, user):
        if user.id != self.request.user.id:
            messages.error(self.request, gettext_lazy('You do not have permission to edit another user.'))
            return False
        return True

class UserListView(ListView):
    model = CustomUser
    template_name = 'users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authenticated_user_id"] = self.request.user.id if self.request.user.is_authenticated else None
        return context

class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            validate_password(form.cleaned_data['password1'])
        except ValidationError as e:
            for error in e:
                messages.error(self.request, error)
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        messages.success(self.request, gettext_lazy("User successfully registered."))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class UserUpdateView(UpdateView, UserPermissionMixin):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "update.html"
    context_object_name = 'user'
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        user = form.save(commit=False)

        password = form.cleaned_data.get('password1')
        if password:
            user.set_password(password)

        user.save()
        return super().form_valid(form)
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser,id=self.kwargs['pk'])

        if not self.check_user_permission(user):
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.kwargs['pk'])

class UserDeleteView(DeleteView, UserPermissionMixin):
    model = CustomUser
    template_name = 'confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser,id=self.kwargs['pk'])

        if not self.check_user_permission(user):
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, gettext_lazy("User has been deleted successfully."))
        return super().delete(request, *args, **kwargs)
