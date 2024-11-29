import django_filters
from .models import Task
from django.utils.translation import gettext_lazy


class TaskFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='icontains')
    performer = django_filters.CharFilter(lookup_expr='icontains')
    label = django_filters.CharFilter(lookup_expr='icontains')
    my_tasks = django_filters.BooleanFilter(method="filter_my_tasks",label=gettext_lazy('Only your tasks'))

    def filter_my_tasks(self,queryset,name,value):
        if value:
            user = getattr(self.request, 'user', None)
            return queryset.filter(creator__username=user.username)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'performer', 'label','my_tasks']