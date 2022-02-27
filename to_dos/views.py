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
        _date = datetime.datetime.strptime(self.request.query_params['date'], '%Y-%m-%d')
        _queryset = self.queryset
        _queryset = _queryset.annotate(
            diff_date=(ExpressionWrapper(_date - F('start_date_time'),
                                         output_field=IntegerField()) / 86400000000),
            diff_month=(_date.month - F('start_date_time__month')),
            daily_repeat_period_condition=(F('diff_date') % Cast('repeat_period', IntegerField())),
            monthly_repeat_period_condition=(F('diff_month') % Cast('repeat_period', IntegerField())),

        )
        _expire_conditions = (
                Q(end_type=EndTypeChoices.NEVER) |
                (Q(end_type=EndTypeChoices.DATE, end_date__gte=_date))
        )
        _not_done_condition = Q(completely_done=False)

        _daily_conditions = Q(
            repeat_type=RepeatTypeChoices.DAY,
            daily_repeat_period_condition=0,
        )
        _monthly_conditions = Q(
            repeat_type=RepeatTypeChoices.MONTH,
            start_date_time__day=_date.day,
            monthly_repeat_period_condition=0,
        )
        _queryset = _queryset.filter(
            _expire_conditions &
            _not_done_condition &
            (
                    _daily_conditions |
                    _monthly_conditions
            )
        )
        return _queryset
