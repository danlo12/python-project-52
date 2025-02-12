import logging

from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.hashers import make_password
from .forms import UserRegistrationForm, UserUpdateForm, CustomLoginForm
from .models import CustomUser
from .mixins import UserPermissionMixin
logger = logging.getLogger(__name__)





class UserListView(ListView):
    model = CustomUser
    template_name = 'users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authenticated_user_id"] = (
            self.request.user.id) \
            if self.request.user.is_authenticated else None
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
        messages.success(self.request,
                         gettext_lazy("User successfully registered."))
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
        (messages.success
         (self.request, gettext_lazy("User successfully changed")))
        user.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.kwargs['pk'])

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
        user = get_object_or_404(CustomUser, id=self.kwargs['pk'])

        if not self.check_user_permission(user):
            return redirect('users')
        if request.method == "POST":
            messages.success(self.request, gettext_lazy("User has been deleted "
                                                        "successfully."))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        for field in form.errors:
            for error in form.errors[field]:
                messages.error(self.request, f"{error}")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
    next_page = reverse_lazy('home')
