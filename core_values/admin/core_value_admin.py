from core.admin import AbstractAdmin


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
