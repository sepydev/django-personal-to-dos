from core.admin import AbstractAdmin


class CoreValueAdmin(AbstractAdmin):
    list_display = [
                       'title',
                       'owner'
                   ] + AbstractAdmin.list_display
    fields = [
                 'title',
                 'description',
                 'owner'
             ] + AbstractAdmin.fields
    raw_id_fields = [
                        'owner',
                    ] + AbstractAdmin.raw_id_fields
