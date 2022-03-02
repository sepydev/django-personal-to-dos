from django.contrib import admin

from .models import Task, PartiallyCompletedTask

admin.site.register(Task)
admin.site.register(PartiallyCompletedTask)
