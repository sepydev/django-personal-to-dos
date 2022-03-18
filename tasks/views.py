from core.views import ModelViewSet, SetOwnerModelViewListMixin, OwnerListModelViewSetMixin
from helpers.swagger import ViewSetTagDecorator
from users.permisions import IsOwnerPermission
from .models import Task as TaskModel, PartiallyCompletedTask as PartiallyCompletedTaskModel
from .serializers import TaskSummarySerializer, TaskDetailSerializer, \
    PartiallyCompletedTaskSummarySerializer, PartiallyCompletedTaskDetailSerializer
from personal_to_dos.tasks.filters import PartiallyCompletedTaskFilter


@ViewSetTagDecorator(tags=("Task",))
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


@ViewSetTagDecorator(tags=("Task",))
class PartiallyCompletedTaskViewSet(SetOwnerModelViewListMixin,
                                    OwnerListModelViewSetMixin,
                                    ModelViewSet):
    permission_classes = (IsOwnerPermission,)
    queryset = PartiallyCompletedTaskModel.objects.all()
    filterset_class = PartiallyCompletedTaskFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return PartiallyCompletedTaskSummarySerializer
        else:
            return PartiallyCompletedTaskDetailSerializer
