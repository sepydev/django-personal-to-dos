from .models import Goal
from django.contrib import admin
from core.admin import AbstractAdmin


class GoalAdmin(AbstractAdmin):
    list_display = [
                       'title',
                       'owner',
                   ] + AbstractAdmin.list_display
    fields = [
                 'title',
                 'description',
                 'owner',
                 'due_date',
                 'core_values',
                 'group'
             ] + AbstractAdmin.fields
    readonly_fields = [] + AbstractAdmin.readonly_fields
    raw_id_fields = [] + AbstractAdmin.raw_id_fields


admin.site.register(Goal, GoalAdmin)
