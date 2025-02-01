import logging

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import CustomLoginForm

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'index.html')


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
