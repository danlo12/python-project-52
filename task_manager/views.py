from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserRegistrationForm, CustomLoginForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

def index(request):
    return render(request,'index.html', context={'who':'Username',})

def user_list(request):
    users = CustomUser.objects.all()
    return render(request,'users.html',{'users':users})

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
            return redirect('home')
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