from django.test import TestCase
from django.contrib.auth import get_user_model
from personal_to_dos.core_values.models import CoreValue as CoreValueModel

UserModel = get_user_model()


def create_user_helper(
        email='test@test.com',
        password='p@123456'
):
    return UserModel.objects.create_user(email, password)


class CoreValueModelTest(TestCase):

    def test_safe_delete(self):
        core_value = CoreValueModel.objects.create(
            title='Test Title',
            user=create_user_helper()
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
            user=create_user_helper()
        )
        core_value.save()
        core_value.delete()
        count_deleted_core_values = CoreValueModel.objects.get_all().filter(is_deleted=True).count()
        self.assertEqual(count_deleted_core_values, 1)
        CoreValueModel.objects.get_all().first().restore()
        count_deleted_core_values = CoreValueModel.objects.get_all().filter(is_deleted=True).count()
        self.assertEqual(count_deleted_core_values, 0)
