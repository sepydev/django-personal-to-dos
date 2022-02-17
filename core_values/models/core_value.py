from django.contrib.auth import get_user_model
from django.db import models

from core.models import AbstractManager, AbstractModel

UserModel = get_user_model()


class CoreValueManager(AbstractManager):
    def get_queryset(self):
        return super(CoreValueManager, self).get_queryset()


class CoreValue(AbstractModel):
    title = models.CharField(
        max_length=200,
        verbose_name='Title'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        verbose_name='User',
    )

    objects = CoreValueManager()

    class Meta:
        verbose_name = 'Core value'
        verbose_name_plural = 'Core values'
