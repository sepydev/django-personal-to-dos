from core.seralizers import AbstractDetailSerializer, AbstractSummarySerializer
from core.seralizers import ChoiceField, MultipleChoiceField
from .models import Task as TaskModel, \
    PartiallyCompletedTask as PartiallyCompletedTaskModel, \
    RepeatTypeChoices, EndTypeChoices, WeekDaysChoices
from rest_framework import serializers


class TaskSummarySerializer(AbstractSummarySerializer):
    goal = serializers.StringRelatedField()
    start_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    repeat_type = ChoiceField(choices=RepeatTypeChoices.choices, )

    class Meta:
        model = TaskModel
        fields = [
            'title',
            'description',
            'owner',
            'goal',
            'start_date_time',
            'completely_done',
            'repeat_type',

            *AbstractSummarySerializer.Meta.fields
        ]
        read_only_fields = [
            'owner',
            *AbstractSummarySerializer.Meta.read_only_fields
        ]


class TaskDetailSerializer(TaskSummarySerializer, AbstractDetailSerializer):
    end_type = ChoiceField(choices=EndTypeChoices.choices)
    selected_week_days = MultipleChoiceField(choices=WeekDaysChoices.choices, )
    repeat_type = ChoiceField(choices=RepeatTypeChoices.choices, )
    start_date_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    goal = None
    goal_title = serializers.StringRelatedField(source="goal")

    class Meta:
        model = TaskModel
        fields = [
            *TaskSummarySerializer.Meta.fields,
            'repeat_period',
            'selected_week_days',
            'end_type',
            'end_date',
            'end_after_occurrence',
            'goal_title',
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
