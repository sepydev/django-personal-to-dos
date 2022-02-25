import datetime
import json

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.test_api import create_user_verify_and_login
from .models import Goal as GoalModel
from ..core_values.tests.test_api import create_core_value


def create_goal(client,
                token,
                core_value_id,
                title="Goal Title Test",
                description="description",
                group="immediately",
                due_date=None,
                is_active=True):
    if not due_date:
        due_date = datetime.date.today()
    response = client.post('/personal-to-dos/goal/',
                           {
                               "title": title,
                               "description": description,
                               "group": group,
                               "due_date": due_date,
                               "is_active": is_active,
                               "core_values": [core_value_id, ]
                           },
                           headers={
                               'Authorization': token
                           })
    return response


class TestGoalAPI(APITestCase):
    def test_create_goal(self):
        token = create_user_verify_and_login(self.client)
        core_value_response = create_core_value(self.client, token)
        core_value_id = json.loads(core_value_response.content)['pk']
        response = create_goal(self.client, token, core_value_id)
        self.assertContains(response, "pk", status_code=status.HTTP_201_CREATED)
        pk = json.loads(response.content)['pk']
        goal = GoalModel.objects.filter(pk=pk).first()
        self.assertEqual(goal.core_values.first().id, core_value_id)
