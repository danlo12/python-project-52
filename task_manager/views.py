from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
import logging

from .filters import TaskFilter
from .users.forms import UserRegistrationForm, UserUpdateForm
from .forms import CustomLoginForm


logger = logging.getLogger(__name__)

def index(request):
    return render(request,'index.html', context={'who':'Username',})

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
    def form_valid(self, form):
        messages.success(self.request, "Вы разлогинены")
    next_page = reverse_lazy('home')
