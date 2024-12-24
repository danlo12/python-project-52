"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import set_language
from django.contrib import admin
from django.urls import include, path

from hexlet_code.task_manager import views

urlpatterns = [
    path('set-language/', set_language, name='set_language'),
    path('', views.index, name='home'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include('hexlet_code.task_manager.users.urls')),
    path('statuses/',include('hexlet_code.task_manager.statuses.urls')),
    path('labels/',include('hexlet_code.task_manager.labels.urls')),
    path('tasks/',include('hexlet_code.task_manager.tasks.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
]
