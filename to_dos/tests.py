import datetime
import json

from rest_framework import status
from rest_framework.test import APITestCase

from personal_to_dos.core_values.tests.test_api import create_core_value
from personal_to_dos.goals.tests import create_goal
from personal_to_dos.tasks.tests import create_task
from users.tests.test_api import create_user_verify_and_login


class DailyTasksTodoAPI(APITestCase):
    def setUp(self) -> None:
        token = create_user_verify_and_login(self.client)
        core_value_response = create_core_value(self.client, token)
        core_value_id = json.loads(core_value_response.content)['pk']
        goal_response = create_goal(self.client, token, core_value_id)
        goal_id = json.loads(goal_response.content)['pk']
        self.token = token
        self.goal_id = goal_id

    def test_daily_unlimited_task(self):
        """
        Testing get to-do api for a task with this condition
        *daily
        *unlimited
        *repeat every day
        *not completed

        the result have to have this task
        """

        create_task(self.client, self.token, self.goal_id,
                    title="Daily-unlimited",
                    start_date_time=datetime.date.today() - datetime.timedelta(days=20),
                    repeat_type="Day",
                    repeat_period=1,
                    end_type="Never",
                    completely_done=False
                    )

        response = self.client.get(
            '/personal-to-dos/to-do/',
            {
                'date': datetime.date.today()
            },
            headers={
                'Authorization': self.token
            }
        )

        self.assertContains(response, "Daily-unlimited", status_code=status.HTTP_200_OK)
