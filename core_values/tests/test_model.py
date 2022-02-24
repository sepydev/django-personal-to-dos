from django.test import TestCase

from personal_to_dos.core_values.models import CoreValue as CoreValueModel
from users.tests.test_api import create_user_helper


class CoreValueModelTest(TestCase):

    def test_safe_delete(self):
        core_value = CoreValueModel.objects.create(
            title='Test Title',
            owner=create_user_helper()
        )
        core_value.save()
        count_not_deleted_core_values = CoreValueModel.objects.all().count()
        self.assertEqual(count_not_deleted_core_values, 1)
        core_value.delete()
        count_deleted_core_values = CoreValueModel.objects.get_all().filter(is_deleted=True).count()
        count_not_deleted_core_values = CoreValueModel.objects.all().count()
        self.assertEqual(count_deleted_core_values, 1)
        self.assertEqual(count_not_deleted_core_values, 0)

    def test_restore(self):
        core_value = CoreValueModel.objects.create(
            title='Test Title',
            owner=create_user_helper()
        )
        core_value.save()
        core_value.delete()
        count_deleted_core_values = CoreValueModel.objects.get_all().filter(is_deleted=True).count()
        self.assertEqual(count_deleted_core_values, 1)
        CoreValueModel.objects.get_all().first().restore()
        count_deleted_core_values = CoreValueModel.objects.get_all().filter(is_deleted=True).count()
        self.assertEqual(count_deleted_core_values, 0)
