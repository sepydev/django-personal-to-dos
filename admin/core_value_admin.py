from django.contrib import admin

from core.admin import AbstractAdmin
from ..models import CoreValue as CoreValueModel


class CoreValueAdmin(AbstractAdmin):
    list_display = [
                       'title',
                       'user'
                   ] + AbstractAdmin.list_display
    fields = [
                 'title',
                 'description',
                 'user'
             ] + AbstractAdmin.fields
    raw_id_fields = [
                        'user',
                    ] + AbstractAdmin.raw_id_fields


admin.site.register(CoreValueModel, CoreValueAdmin)
