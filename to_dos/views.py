import datetime

from django.db.models import Q, F, ExpressionWrapper, IntegerField
from django.db.models.functions import Cast
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from users.permisions import IsOwnerPermission
from .serializers import ToDoSummarySerializer
from ..tasks.models import Task as TaskModel, RepeatTypeChoices, EndTypeChoices


class TodoAPIView(ListModelMixin, GenericViewSet):
    permission_classes = (IsOwnerPermission,)
    queryset = TaskModel.objects.all()
    serializer_class = ToDoSummarySerializer

    def get_queryset(self):
        _date = self.request.query_params['date']
        _queryset = self.queryset
        _queryset = _queryset.annotate(
            diff_date=(ExpressionWrapper(datetime.datetime.now() - F('start_date_time'),
                                         output_field=IntegerField()) / 86400000000),
            daily_repeat_period_condition=(F('diff_date') % Cast('repeat_period', IntegerField()))
        )
        _daily = (
                Q(repeat_type=RepeatTypeChoices.DAY) &
                (
                        Q(end_type=EndTypeChoices.NEVER) |
                        (Q(end_type=EndTypeChoices.DATE, end_date__gte=_date))
                ) &
                Q(daily_repeat_period_condition=0)
        )
        _queryset = _queryset.filter(_daily)

        return _queryset
