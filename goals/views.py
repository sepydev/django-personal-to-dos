from core.views import ModelViewSet, OwnerListModelViewSetMixin, SetOwnerModelViewListMixin
from helpers.swagger import ViewSetTagDecorator
from users.permisions import IsOwnerPermission
from .serializers import GoalDetailSerializer, GoalSummarySerializer
from ..models import Goal as GoalModel


@ViewSetTagDecorator(tags=("Goal",))
class GoalViewSet(
    OwnerListModelViewSetMixin,
    SetOwnerModelViewListMixin,
    ModelViewSet
):
    queryset = GoalModel.objects.all()
    permission_classes = (IsOwnerPermission,)

    def get_queryset(self):
        queryset = super(GoalViewSet, self).get_queryset()
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('core_values')
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GoalDetailSerializer
        else:
            return GoalSummarySerializer
