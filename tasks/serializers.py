from core.seralizers import AbstractDetailSerializer, AbstractSummarySerializer
from core.seralizers import ChoiceField
from .models import Task as TaskModel, RepeatTypeChoices, EndTypeChoices


class TaskSummarySerializer(AbstractSummarySerializer):
    class Meta:
        model = TaskModel
        fields = [
            'title',
            'description',
            'owner',
            *AbstractSummarySerializer.Meta.fields
        ]
        read_only_fields = [
            'owner',
            *AbstractSummarySerializer.Meta.read_only_fields
        ]


class TaskDetailSerializer(TaskSummarySerializer, AbstractDetailSerializer):
    repeat_type = ChoiceField(choices=RepeatTypeChoices.choices, )
    end_type = ChoiceField(choices=EndTypeChoices.choices)

    class Meta:
        model = TaskModel
        fields = [
            *TaskSummarySerializer.Meta.fields,
            'goal',
            'start_date_time',
            'repeat_type',
            'repeat_period',
            'selected_week_days',
            'end_type',
            'end_date',
            'end_after_occurrence',
            'completely_done',
            *AbstractDetailSerializer.Meta.fields,
        ]
        read_only_fields = [
            *TaskSummarySerializer.Meta.read_only_fields,
            *AbstractDetailSerializer.Meta.read_only_fields,
        ]
