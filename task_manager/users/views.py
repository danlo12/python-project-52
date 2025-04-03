import logging

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CustomLoginForm, UserRegistrationForm, UserUpdateForm
from .mixins import UserPermissionMixin
from .models import CustomUser

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


class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('login')
    success_message = gettext_lazy("User successfully registered.")

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class UserUpdateView(SuccessMessageMixin, UserPermissionMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "update.html"
    context_object_name = 'user'
    success_url = reverse_lazy('users')
    success_message = gettext_lazy("User successfully changed")

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.kwargs['pk'])


class UserDeleteView(SuccessMessageMixin, UserPermissionMixin, DeleteView):
    model = CustomUser
    template_name = 'confirm_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users')
    success_message = gettext_lazy("User has been deleted successfully.")


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')
    success_message = gettext_lazy("You are logged in")


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, gettext_lazy("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
