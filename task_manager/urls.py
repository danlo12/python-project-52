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
from django.urls import path, include
from task_manager import views
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('set-language/', set_language, name='set_language'),
    path('', views.index, name='home'),
    path('users/', views.user_list, name='users'),
    path('users/create/', views.user_create, name='user-create'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/', views.LogoutView.as_view(next_page='home'), name='logout'),
    path('users/<int:pk>/update/',views.UserUpdateView.as_view(),name='update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='delete_user'),
    path("i18n/", include("django.conf.urls.i18n")),
    path('admin/', admin.site.urls),
    path('statuses/',views.StatusesListView.as_view(),name='statuses'),
    path('statuses/create/',views.StatusesCreateView.as_view(),name='status_create'),
    path('statuses/<int:pk>/update/',views.StatusesUpdateView.as_view(),name='status_update'),
    path('statuses/<int:pk>/delete/',views.StatusesDeleteView.as_view(),name='status_delete'),
]
