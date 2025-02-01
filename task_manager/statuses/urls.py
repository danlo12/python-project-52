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
from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path('',views.StatusesListView.as_view(),name='statuses'),
    path('create/',views.StatusesCreateView.as_view(),name='status_create'),
    path('<int:pk>/update/',views.StatusesUpdateView.as_view(),name='status_update'),
    path('<int:pk>/delete/',views.StatusesDeleteView.as_view(),name='status_delete'),

]
