from core.seralizers import AbstractSummarySerializer, AbstractDetailSerializer
from .models import Goal as GoalModel
from ..core_values.serializers import CoreValueSummarySerializer


class GoalSummarySerializer(AbstractSummarySerializer):
    class Meta:
        model = GoalModel
        fields = [
                     'title',
                     'description',
                     'group',
                     'due_date'
                 ] + AbstractSummarySerializer.Meta.fields
        read_only_fields = [] + AbstractSummarySerializer.Meta.read_only_fields


class GoalDetailSerializer(GoalSummarySerializer, AbstractDetailSerializer):
    core_values = CoreValueSummarySerializer(many=True)

    class Meta:
        model = GoalModel
        fields = ['core_values'] + \
                 GoalSummarySerializer.Meta.fields + \
                 AbstractDetailSerializer.Meta.fields
        read_only_fields = [] + \
                           GoalSummarySerializer.Meta.read_only_fields + \
                           AbstractDetailSerializer.Meta.read_only_fields
