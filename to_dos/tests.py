import datetime
import json

from rest_framework import status
from rest_framework.test import APITestCase

from helpers.date_time import add_months, add_years, add_days
from personal_to_dos.core_values.tests.test_api import create_core_value
from personal_to_dos.goals.tests import create_goal
from personal_to_dos.tasks.tests import create_task
from users.tests.test_api import create_user_verify_and_login


class TodoAPIMixin:

    def setUp(self) -> None:
        token = create_user_verify_and_login(self.client)
        core_value_response = create_core_value(self.client, token)
        core_value_id = json.loads(core_value_response.content)['pk']
        goal_response = create_goal(self.client, token, core_value_id)
        goal_id = json.loads(goal_response.content)['pk']
        self.token = token
        self.goal_id = goal_id


class TestExpireAndDoneTasks(TodoAPIMixin, APITestCase):

    def test_expired_task(self):
        """
        Testing get to-do api for a task with this condition
        *daily
        *expired
        *repeat every day
        *not completed

        This task does not have to be in the result
        """

        create_task(self.client, self.token, self.goal_id,
                    title="Daily-expired-today",
                    start_date_time=add_days(datetime.date.today(), -20),
                    repeat_type="Day",
                    repeat_period=1,
                    end_type="On Specific date",
                    end_date=add_days(datetime.date.today(), -1),
                    completely_done=False
                    )

        create_task(self.client, self.token, self.goal_id,
                    title="Daily-expired-last-week",
                    start_date_time=add_days(datetime.date.today(), -20),
                    repeat_type="Day",
                    repeat_period=1,
                    end_type="On Specific date",
                    end_date=add_days(datetime.date.today(), -7),
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

        self.assertNotContains(response, "Daily-expired", status_code=status.HTTP_200_OK)

        response = self.client.get(
            '/personal-to-dos/to-do/',
            {
                'date': add_days(datetime.date.today(), -3)
            },
            headers={
                'Authorization': self.token
            }
        )

        self.assertContains(response, "Daily-expired-today", status_code=status.HTTP_200_OK)
        self.assertNotContains(response, "Daily-expired-last-week", status_code=status.HTTP_200_OK)

    def test_done_task(self):
        create_task(self.client, self.token, self.goal_id,
                    title="task completely done",
                    start_date_time=add_days(datetime.date.today(), 20),
                    repeat_type="Day",
                    repeat_period=1,
                    end_type="On Specific date",
                    end_date=datetime.date.today() + datetime.timedelta(days=101),
                    completely_done=True
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

        self.assertNotContains(response, "task completely done", status_code=status.HTTP_200_OK)


class TestDailyTasks(TodoAPIMixin, APITestCase):

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
                    start_date_time=add_days(datetime.date.today(), -20),
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

    def test_daily_task_repeat_period(self):
        create_task(self.client, self.token, self.goal_id,
                    title="Daily-not-contains-repeat_period=2",
                    start_date_time=add_days(datetime.date.today(), -1),
                    repeat_type="Day",
                    repeat_period=2,
                    end_type="Never",
                    completely_done=False
                    )
        create_task(self.client, self.token, self.goal_id,
                    title="Daily-not-contains-repeat_period=3",
                    start_date_time=add_days(datetime.date.today(), -1),
                    repeat_type="Day",
                    repeat_period=3,
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

        self.assertNotContains(response, "Daily-not-contains-repeat_period=2", status_code=status.HTTP_200_OK)
        self.assertNotContains(response, "Daily-not-contains-repeat_period=3", status_code=status.HTTP_200_OK)


class TestMonthlyTasks(TodoAPIMixin, APITestCase):

    def test_monthly_unlimited_task(self):
        create_task(self.client, self.token, self.goal_id,
                    title="Monthly-unlimited",
                    start_date_time=add_months(datetime.date.today(), -1),
                    repeat_type="Month",
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

        self.assertContains(response, "Monthly-unlimited", status_code=status.HTTP_200_OK)

    def test_monthly_task_repeat_period(self):
        create_task(self.client, self.token, self.goal_id,
                    title="Monthly-not-contains-repeat_period=2",
                    start_date_time=add_months(datetime.date.today(), -1),
                    repeat_type="Month",
                    repeat_period=2,
                    end_type="Never",
                    completely_done=False
                    )
        create_task(self.client, self.token, self.goal_id,
                    title="Monthly-not-contains-repeat_period=3",
                    start_date_time=add_months(datetime.date.today(), -1),
                    repeat_type="Month",
                    repeat_period=3,
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

        self.assertNotContains(response, "Monthly-not-contains-repeat_period=2", status_code=status.HTTP_200_OK)
        self.assertNotContains(response, "Monthly-not-contains-repeat_period=3", status_code=status.HTTP_200_OK)


class TestYearlyTasks(TodoAPIMixin, APITestCase):

    def test_yearly_unlimited_task(self):
        create_task(self.client, self.token, self.goal_id,
                    title="Yearly-unlimited",
                    start_date_time=add_years(datetime.date.today(), -1),
                    repeat_type="Year",
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

        self.assertContains(response, "Yearly-unlimited", status_code=status.HTTP_200_OK)

    def test_monthly_task_repeat_period(self):
        create_task(self.client, self.token, self.goal_id,
                    title="Yearly-not-contains-repeat_period=2",
                    start_date_time=add_years(datetime.date.today(), -1),
                    repeat_type="Year",
                    repeat_period=2,
                    end_type="Never",
                    completely_done=False
                    )
        create_task(self.client, self.token, self.goal_id,
                    title="Yearly-not-contains-repeat_period=3",
                    start_date_time=add_years(datetime.date.today(), -1),
                    repeat_type="Year",
                    repeat_period=3,
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

        self.assertNotContains(response, "Yearly-not-contains-repeat_period=2", status_code=status.HTTP_200_OK)
        self.assertNotContains(response, "Yearly-not-contains-repeat_period=3", status_code=status.HTTP_200_OK)
