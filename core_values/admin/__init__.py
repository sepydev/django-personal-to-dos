from .core_value_admin import CoreValueAdmin
from django.contrib import admin
from personal_to_dos.core_values.models import CoreValue as CoreValueModel

admin.site.register(CoreValueModel, CoreValueAdmin)
