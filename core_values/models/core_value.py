from core.models import AbstractManager, AbstractModel, TitleDescriptionModelMixin, OwnerModelMixin


class CoreValueManager(AbstractManager):
    def get_queryset(self):
        return super(CoreValueManager, self).get_queryset()


class CoreValue(TitleDescriptionModelMixin, OwnerModelMixin, AbstractModel):
    objects = CoreValueManager()

    class Meta:
        verbose_name = 'Core value'
        verbose_name_plural = 'Core values'
