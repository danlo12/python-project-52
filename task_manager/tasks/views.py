import logging

from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.tasks.filters import TaskFilter

from .models import CustomUser, Label, Status, Task

logger = logging.getLogger(__name__)


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get('status')
        performer = self.request.GET.get('performer')
        label = self.request.GET.get('labels')
        my_tasks = self.request.GET.get('my_tasks')

        if status:
            queryset = queryset.filter(status__name=status)
        if performer:
            queryset = queryset.filter(performer__id=performer)
        if label:
            queryset = queryset.filter(labels__id=label)
        if my_tasks == "on":
            queryset = queryset.filter(creator=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = (
            Task.objects.values_list('status__name', flat=True).distinct())
        context['performers'] = CustomUser.objects.all().distinct()
        context['labels'] = Label.objects.all()
        context['current_filters'] = {
            'status': self.request.GET.get('status', ''),
            'performer': self.request.GET.get('performer', ''),
            'labels': self.request.GET.get('labels', ''),
            'my_tasks': self.request.GET.get('my_tasks', ''),
        }
        return context


class TasksCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks_create.html'
    fields = ['name', 'description', 'status', 'performer', 'labels']
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')
    login_url = "/login"

    def handle_no_permission(self):
        messages.error(self.request, gettext_lazy(
            'You need to be logged in to perform this action.'))
        return super().handle_no_permission()

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.success(request, gettext_lazy('Task successfully create'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['labels'] = Label.objects.all()
        context['performers'] = CustomUser.objects.all()
        return context

    def form_valid(self, form):
        form.instance.creator = self.request.user
        print(self.request.POST.getlist('labels'))
        return super().form_valid(form)


class TasksUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    template_name = 'tasks_update.html'
    fields = ['name', 'description', 'status', 'performer', 'labels']
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    login_url = "/login"
    permission_required = 'tasks.update_task'
    raise_exception = False

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, gettext_lazy(
                'You need to be logged in to perform this action.'))
            return super().handle_no_permission()
        else:
            messages.error(self.request, gettext_lazy('You do not have permission to update this task.'))
            return redirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.success(request, gettext_lazy('Task successfully update'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['statuses'] = Status.objects.all()
        context['labels'] = Label.objects.all()
        context['task_labels'] = (
            list(task.labels.values_list('id', flat='True')))
        context['performers'] = CustomUser.objects.all()
        return context


class TasksDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks_delete.html'
    success_url = reverse_lazy('tasks')
    login_url = "/login"
    permission_required = 'tasks.delete_task'
    raise_exception = False

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request, gettext_lazy(
                'You need to be logged in to perform this action.'))
            return super().handle_no_permission()
        else:
            messages.error(self.request, gettext_lazy('You do not have permission to delete this task.'))
            return redirect(self.success_url)

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            messages.success(request, gettext_lazy('Task successfully delete'))
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_card.html'
    context_object_name = 'task'
