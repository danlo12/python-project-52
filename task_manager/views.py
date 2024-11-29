from cProfile import label

from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, Status, Task, Label
from .forms import UserRegistrationForm, CustomLoginForm, UserUpdateForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy
from django.views.generic import ListView
from .filters import TaskFilter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def index(request):
    return render(request,'index.html', context={'who':'Username',})

def user_list(request):
    users = CustomUser.objects.all()
    user_id = request.user.id if request.user.is_authenticated else None
    return render(request,'users.html',{'users':users,"authenticated_user_id":user_id})

def user_create(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()

    return render(request, 'user_create.html',{'form':form})

class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class UserUpdateView(UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = "update.html"
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        user = form.save(commit=False)

        password = form.cleaned_data.get('password')
        if password:
            user.set_password(password)

        user.save()
        return super().form_valid(form)
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser,id=self.kwargs['pk'])

        if user.id != request.user.id:
            messages.error(request, gettext_lazy('You do not have permission to edit another user.'))
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()

        context['user_id'] = user.id
        context['first_name'] = user.first_name
        context['last_name'] = user.last_name
        context['username'] = user.username

        return context

class UserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser,id=self.kwargs['pk'])

        if user.id != request.user.id:
            messages.error(request, gettext_lazy('You do not have permission to edit another user.'))
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "User has been deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()

        context['user_id'] = user.id
        context['username'] = user.username

        return context

class StatusesListView(ListView):
    model = Status
    template_name = 'statuses.html'
    context_object_name = 'statuses'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class StatusesCreateView(CreateView):
    model = Status
    template_name = 'status_create.html'
    fields = ['name']
    context_object_name = 'statuses'
    success_url = reverse_lazy('statuses')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class StatusesUpdateView(UpdateView):
    model = Status
    template_name = 'status_update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class StatusesDeleteView(DeleteView):
    model = Status
    template_name = 'status_delete.html'
    success_url = reverse_lazy('statuses')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

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

class LabelsListView(ListView):
    model = Label
    template_name = 'labels.html'
    context_object_name = 'labels'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class LabelsCreateView(CreateView):
    model = Label
    template_name = 'label_create.html'
    fields = ['name']
    context_object_name = 'labels'
    success_url = reverse_lazy('labels')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class LabelsUpdateView(UpdateView):
    model = Label
    template_name = 'label_update.html'
    fields = ['name']
    success_url = reverse_lazy('labels')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class LabelsDeleteView(DeleteView):
    model = Label
    template_name = 'label_delete.html'
    success_url = reverse_lazy('labels')
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, gettext_lazy('You need to be logged in to perform this action.'))
            return redirect('login')
        label = self.get_object()
        if label.task_set.exists():
            messages.error(request, gettext_lazy('Cannot delete label because it is associated with tasks.'))
            return redirect('labels')
        return super().dispatch(request, *args, **kwargs)