from core.views import ModelViewSet, OwnerListModelViewSetMixin, SetOwnerModelViewListMixin
from helpers.swagger import ViewSetTagDecorator
from users.permisions import IsOwnerPermission
from ..models import CoreValue as CoreValueModel
from ..serializers import CoreValueSummarySerializer, CoreValueDetailSerializer


@ViewSetTagDecorator(tags=("Core Value",))
class CoreValueViewSet(
    OwnerListModelViewSetMixin,
    SetOwnerModelViewListMixin,
    ModelViewSet
):
    queryset = CoreValueModel.objects.all()
    permission_classes = (IsOwnerPermission,)
    serializer_class = CoreValueSummarySerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoreValueDetailSerializer
        return CoreValueSummarySerializer
