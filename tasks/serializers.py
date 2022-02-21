from core.seralizers import AbstractDetailSerializer, AbstractSummarySerializer
from .models import Task as TaskModel


class TaskSummarySerializer(AbstractSummarySerializer):
    class Meta:
        model = TaskModel
        fields = [
            'title',
            'description',
            'owner',
            *AbstractSummarySerializer.fields
        ]
        read_only_fields = [
            'owner',
            *AbstractSummarySerializer.fields
        ]


class TaskDetailSerializer(TaskSummarySerializer, AbstractDetailSerializer):
    class Meta:
        model = TaskModel
        fields = [
            *TaskSummarySerializer.fields,
            'goal',
            'start_date_time',
            'repeat_type',
            'repeat_period',
            'selected_week_days',
            'end_type',
            'end_date',
            'end_after_occurrence',
            'completely_done',
            *AbstractDetailSerializer.fields,
        ]
        read_only_fields = [
            *TaskSummarySerializer.fields,
            *AbstractDetailSerializer.fields,
        ]
