from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from users.permisions import IsOwnerPermission
from ..tasks.models import Task as TaskModel
from .serializers import ToDoSummarySerializer


class TodoAPIView(ListModelMixin, GenericViewSet):
    permission_classes = (IsOwnerPermission,)
    queryset = TaskModel.objects.all()
    serializer_class = ToDoSummarySerializer
