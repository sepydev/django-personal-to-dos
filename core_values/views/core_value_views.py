from rest_framework.viewsets import ModelViewSet
from ..models import CoreValue as CoreValueModel
from rest_framework.permissions import IsAuthenticated
from ..serializers import CoreValueSummarySerializer, CoreValueDetailSerializer


class CoreValueViewSet(ModelViewSet):
    queryset = CoreValueModel.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CoreValueSummarySerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoreValueDetailSerializer
        return CoreValueSummarySerializer
