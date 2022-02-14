from core.seralizers import AbstractDetailSerializer, AbstractSummarySerializer
from ..models import CoreValue as CoreValueModel


class CoreValueSummarySerializer(AbstractSummarySerializer):
    class Meta:
        model = CoreValueModel
        fields = [
                     'title',
                     'description',
                     'user'

                 ] + AbstractSummarySerializer.Meta.fields
        read_only_fields = [] + AbstractSummarySerializer.Meta.read_only_fields


class CoreValueDetailSerializer(CoreValueSummarySerializer, AbstractDetailSerializer):
    class Meta:
        model = CoreValueModel
        fields = [] + \
            CoreValueSummarySerializer.Meta.fields + \
            AbstractDetailSerializer.Meta.fields

        read_only_fields = [] + \
            CoreValueSummarySerializer.Meta.read_only_fields + \
            AbstractDetailSerializer.Meta.read_only_fields
