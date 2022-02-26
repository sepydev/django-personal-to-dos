from core.seralizers import AbstractSummarySerializer
from ..tasks.models import Task as TaskModel


class ToDoSummarySerializer(AbstractSummarySerializer):
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
