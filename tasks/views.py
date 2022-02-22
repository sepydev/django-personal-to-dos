from core.views import ModelViewSet, SetOwnerModelViewListMixin, OwnerListModelViewSetMixin
from users.permisions import IsOwnerPermission
from .serializers import TaskSummarySerializer, TaskDetailSerializer
from .models import Task as TaskModel


class TaskViewSet(SetOwnerModelViewListMixin,
                  OwnerListModelViewSetMixin,
                  ModelViewSet):
    permission_classes = (IsOwnerPermission,)
    queryset = TaskModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskSummarySerializer
        else:
            return TaskDetailSerializer
