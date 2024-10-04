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
from django.contrib import admin
from django.urls import path
from task_manager import views


urlpatterns = [
    path('', views.index, name='home'),
    path('users/', views.user_list, name='users'),
    path('users/create/', views.user_create, name='user-create'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(next_page='home'), name='logout'),
    path('users/<int:id>/update/',views.UserUpdateView.as_view(),name='update'),
    path('user/delete/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
    path('admin/', admin.site.urls),
]
