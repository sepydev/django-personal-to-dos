from rest_framework import serializers

from core.seralizers import AbstractSummarySerializer
from ..tasks.models import Task as TaskModel


class ToDoSummarySerializer(AbstractSummarySerializer):
    done_today = serializers.BooleanField()
    goal = serializers.StringRelatedField()

    class Meta:
        model = TaskModel
        fields = [
            'title',
            'description',
            'goal',
            'owner',
            'done_today',
            *AbstractSummarySerializer.Meta.fields
        ]
        read_only_fields = [
            'title',
            'description',
            'goal',
            'owner',
            'done_today',
            *AbstractSummarySerializer.Meta.read_only_fields
        ]
