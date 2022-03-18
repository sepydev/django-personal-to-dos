from django_filters import rest_framework as filters

from personal_to_dos.tasks.models import PartiallyCompletedTask as PartiallyCompletedTaskModel


class PartiallyCompletedTaskFilter(filters.FilterSet):
    date = filters.DateTimeFilter(field_name="create_date")
    task_id = filters.NumberFilter(field_name="task")

    class Meta:
        model = PartiallyCompletedTaskModel
        fields = ['date', 'task_id']
