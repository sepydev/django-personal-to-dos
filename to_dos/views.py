import datetime

from django.db.models import Q, F, ExpressionWrapper, IntegerField

from django.db.models.functions import Cast, ExtractDay, ExtractMonth, ExtractYear
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from helpers.date_time import add_days
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

        # _queryset = _queryset.annotate(
        #     p=ExtractDay(_date - F('start_date_time')),
        # )
        #
        # return _queryset

        _queryset = _queryset.annotate(
            diff_date=ExtractDay(_date - F('start_date_time')),
            diff_month=(_date.month - F('start_date_time__month')),
            diff_year=(_date.year - F('start_date_time__year')),
            diff_week=((F('diff_date') + F('start_date_time__week_day') - _date.weekday()) / 7),
            daily_repeat_period_condition=Cast(F('diff_date') % Cast('repeat_period', IntegerField()), IntegerField()),
            monthly_repeat_period_condition=Cast(F('diff_month') % Cast('repeat_period', IntegerField()),
                                                 IntegerField()),
            yearly_repeat_period_condition=Cast(F('diff_year') % Cast('repeat_period', IntegerField()), IntegerField()),
            weekly_repeat_period_condition=Cast(F('diff_week') % Cast('repeat_period', IntegerField()), IntegerField()),
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
        _yearly_conditions = Q(
            repeat_type=RepeatTypeChoices.YEAR,
            start_date_time__day=_date.day,
            start_date_time__month=_date.month,
            yearly_repeat_period_condition=0,
        )
        _weekly_conditions = Q(
            repeat_type=RepeatTypeChoices.WEEK,
            selected_week_days__contains=[_date.strftime("%A")[:2], ],
            weekly_repeat_period_condition=0,
        )

        _queryset = _queryset.filter(
            _expire_conditions &
            _not_done_condition &
            (
                    _daily_conditions |
                    _monthly_conditions |
                    _yearly_conditions |
                    _weekly_conditions
            )
        )
        return _queryset
