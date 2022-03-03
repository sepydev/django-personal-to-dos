from core.seralizers import AbstractDetailSerializer, AbstractSummarySerializer
from core.seralizers import ChoiceField, MultipleChoiceField
from .models import Task as TaskModel, \
    PartiallyCompletedTask as PartiallyCompletedTaskModel, \
    RepeatTypeChoices, EndTypeChoices, WeekDaysChoices


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
    selected_week_days = MultipleChoiceField(choices=WeekDaysChoices.choices, )

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


class PartiallyCompletedTaskSummarySerializer(AbstractSummarySerializer):
    class Meta:
        model = PartiallyCompletedTaskModel
        fields = [
            'description',
            'owner',
            'task',
            *AbstractSummarySerializer.Meta.fields
        ]
        read_only_fields = [
            'owner',
            *AbstractSummarySerializer.Meta.read_only_fields
        ]


class PartiallyCompletedTaskDetailSerializer(PartiallyCompletedTaskSummarySerializer, AbstractDetailSerializer):
    class Meta:
        model = PartiallyCompletedTaskModel
        fields = [
            *PartiallyCompletedTaskSummarySerializer.Meta.fields,
            *AbstractDetailSerializer.Meta.fields,
        ]
        read_only_fields = [
            *PartiallyCompletedTaskSummarySerializer.Meta.read_only_fields,
            *AbstractDetailSerializer.Meta.read_only_fields,
        ]
