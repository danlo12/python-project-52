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
from .models import CustomUser, Label, Status, Task


logger = logging.getLogger(__name__)



class TasksListView(ListView):
    model = Task
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get('status')
        performer = self.request.GET.get('performer')
        label = self.request.GET.get('label')
        my_tasks = self.request.GET.get('my_tasks')

        if status:
            queryset = queryset.filter(status__name=status)
        if performer:
            queryset = queryset.filter(performer__username=performer)
        if label:
            queryset = queryset.filter(label=label)
        if my_tasks == "on":
            queryset = queryset.filter(creator=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

            # Добавляем данные для фильтров
        context['statuses'] = Task.objects.values_list('status__name', flat=True).distinct()
        context['performers'] = Task.objects.values_list('performer__username', flat=True).distinct()
        context['labels'] = Task.objects.values_list('labels__name', flat=True).distinct()

            # Передаем текущие фильтры в шаблон для сохранения состояния
        context['current_filters'] = {
            'status': self.request.GET.get('status', ''),
            'performer': self.request.GET.get('performer', ''),
            'label': self.request.GET.get('label', ''),
            'my_tasks': self.request.GET.get('my_tasks', ''),
        }
        return context

class TasksCreateView(CreateView):
    model = Task
    template_name = 'tasks_create.html'
    fields = ['name','description','status','performer','labels']
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
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



class TasksUpdateView(UpdateView):
    model = Task
    template_name = 'tasks_update.html'
    fields = ['name','description','status','performer','labels']
    context_object_name = 'tasks'
    success_url = reverse_lazy('tasks')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['labels'] = Label.objects.all()
        context['performers'] = CustomUser.objects.all()
        return context

class TasksDeleteView(DeleteView):
    model = Task
    template_name = 'tasks_delete.html'
    success_url = reverse_lazy('tasks')

    def dispatch(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=self.kwargs['pk'])

        if task.creator.id != request.user.id:
            messages.error(request, gettext_lazy('You do not have permission to edit this task.'))
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_card.html'
    context_object_name = 'task'