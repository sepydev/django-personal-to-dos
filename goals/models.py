from django.db import models

from core.models import AbstractModel, OwnerModelMixin, TitleDescriptionModelMixin, AbstractManager
from ..models import CoreValue


class GoalManager(AbstractManager):
    def get_queryset(self):
        return super(GoalManager, self).get_queryset()


class GroupChoices(models.TextChoices):
    IMMEDIATELY = ('immediately', "Immediately")
    SHORT_TERM = ('short term', 'Short term')
    MIDDLE_TERM = ('middle term', 'Middle term')
    LONG_TERM = ('long term', 'Long term')
    VERY_LONG_TERM = ('Very Long term', 'Very Long term')


class Goal(TitleDescriptionModelMixin, OwnerModelMixin, AbstractModel):
    due_date = models.DateField(
        verbose_name="Due date",
        blank=True,
        null=True
    )
    core_values = models.ManyToManyField(
        CoreValue,
        verbose_name="Core values",
    )
    group = models.CharField(
        max_length=30,
        verbose_name="Group",
        blank=True,
        null=True,
        choices=GroupChoices.choices
    )

    objects = GoalManager()
