from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.test_api import create_user_verify_and_login
from ..models import CoreValue


def create_core_value(client,
                      token,
                      title="core value title",
                      description="description",
                      is_active=True):
    return client.post(
        '/personal-to-dos/core-value/',
        {
            "title": title,
            "description": description,
            "is_active": is_active
        },
        headers={
            'Authorization': token
        }
    )


class CoreValuesAPI(APITestCase):
    def test_create(self):
        """Test creating new core value via API"""

        token = create_user_verify_and_login(self.client)
        response = create_core_value(self.client, token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        core_value_count = CoreValue.objects.count()
        self.assertEqual(core_value_count, 1)
