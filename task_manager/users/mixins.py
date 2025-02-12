from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy
from .models import CustomUser


class UserPermissionMixin:
    def check_user_permission(self, user):
        if user.id != self.request.user.id:
            messages.error(self.request,
                           gettext_lazy('You do not have '
                                        'permission to edit another user.'))
            return False
        return True
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=self.kwargs['pk'])

        if not self.check_user_permission(user):
            return redirect('users')