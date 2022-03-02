from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from core.models import AbstractModel, OwnerModelMixin, TitleDescriptionModelMixin, AbstractManager
from ..goals.models import Goal as GoalModel


class RepeatTypeChoices(models.IntegerChoices):
    NO_REPEAT = (0, "No repeat")
    DAY = (1, "Day")
    WEEK = (2, "Week")
    MONTH = (3, "Month")
    YEAR = (4, "Year")


class EndTypeChoices(models.IntegerChoices):
    NEVER = (0, "Never")
    DATE = (1, "On Specific date")
    OCCURRENCES = (2, "After specific occurrence")


class WeekDaysChoices(models.TextChoices):
    SUNDAY = ("Su", "Sunday")
    MONDAY = ("Mo", "Monday")
    TUESDAY = ("Tu", "Tuesday")
    WEDNESDAY = ("We", "Wednesday")
    THURSDAY = ("Th", "Thursday")
    FRIDAY = ("Fr", "Friday")
    SATURDAY = ("Sa", "Saturday")


class TaskManager(AbstractManager):
    def get_queryset(self):
        return super(TaskManager, self).get_queryset()


class Task(
    TitleDescriptionModelMixin,
    OwnerModelMixin,
    AbstractModel
):
    goal = models.ForeignKey(
        GoalModel,
        on_delete=models.CASCADE,
        verbose_name="Related Goal",
        blank=True,
        null=True,
    )
    start_date_time = models.DateTimeField(
        verbose_name="Start date time",
    )
    repeat_type = models.PositiveSmallIntegerField(
        choices=RepeatTypeChoices.choices,
        verbose_name="Repeat Type",
    )
    repeat_period = models.IntegerField(
        verbose_name="Repeat period",
        blank=True,
        null=True,
    )

    selected_week_days = models.JSONField(
        verbose_name="Selected week days",
        default=[],
        blank=True,
        null=True,

    )
    end_type = models.PositiveSmallIntegerField(
        choices=EndTypeChoices.choices,
        verbose_name="End repeat type",
        blank=True,
        null=True,
    )
    end_date = models.DateField(
        verbose_name="End date",
        blank=True,
        null=True,
    )
    end_after_occurrence = models.PositiveIntegerField(
        verbose_name="End after occurrence",
        blank=True,
        null=True,
    )

    completely_done = models.BooleanField(
        default=False,
        verbose_name="Task is completely done"
    )

    objects = TaskManager()

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def clean_repeat_type(self):
        """Clean fields related to repeat type"""

        if self.repeat_type == RepeatTypeChoices.NO_REPEAT.value:
            self.repeat_period = None
            self.selected_week_days = None
            self.end_type = None
            self.end_date = None
            self.end_after_occurrence = None
        else:
            # Check repeat is mandatory if repeat type not equal NO_REPEAT
            if self.repeat_period is None:
                raise ValidationError(
                    {
                        'repeat_period': _('Repeat period is mandatory')
                    },
                    code='mandatory'
                )

    def clean_end_type(self):
        """Clean fields  related to end type"""
        if self.end_type == EndTypeChoices.NEVER.value:
            self.end_date = None
            self.end_after_occurrence = None
        elif self.end_type == EndTypeChoices.DATE.value and self.end_date is None:
            raise ValidationError(
                {
                    'end_date': _('End date is mandatory')
                },
                code='mandatory'
            )
        elif self.end_type == EndTypeChoices.OCCURRENCES.value and self.end_after_occurrence is None:
            raise ValidationError(
                {
                    'end_after_occurrence': _('End after occurrence is mandatory')
                },
                code='mandatory'
            )

    def clean_selected_week_days(self):
        """Make sure repeat_week_day field is like this ['Su','Mo','Tu','We','Th','Fr','Sa']"""
        if self.repeat_type == RepeatTypeChoices.WEEK:
            self.selected_week_days = list(set(self.selected_week_days))
            if not isinstance(self.selected_week_days, list):
                raise ValidationError(
                    {
                        'selected_week_days':
                            _('This field has to be a list'
                              ),
                    },
                    code='invalid'
                )
            for item in self.selected_week_days:
                if not isinstance(item, str):
                    raise ValidationError(
                        {
                            'selected_week_days': _('Items of this field have to be string')
                        },
                        code='invalid'
                    )
            if not self.selected_week_days:
                raise ValidationError(
                    {
                        'selected_week_days':
                            _("You have to select at least one of these items:['Su','Mo','Tu','We','Th','Fr','Sa'] "
                              )
                    }, code='mandatory'
                )
            if set(self.selected_week_days) - set(WeekDaysChoices.values):
                raise ValidationError(
                    {
                        'selected_week_days': ValidationError(
                            _("You can only choice these items : ['Su','Mo','Tu','We','Th','Fr','Sa'] "
                              ), code='invalid')
                    }
                )

    def clean(self):
        self.clean_repeat_type()
        self.clean_end_type()
        self.clean_selected_week_days()
