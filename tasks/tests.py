import datetime
import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.test_api import create_user_verify_and_login
from .models import Task as TaskModel
from ..core_values.tests.test_api import create_core_value
from ..goals.tests import create_goal

UserModel = get_user_model()


class PrepareTaskTestMixin:

    def setUp(self) -> None:
        token = create_user_verify_and_login(self.client)
        core_value_response = create_core_value(self.client, token)
        core_value_id = json.loads(core_value_response.content)['pk']
        goal_response = create_goal(self.client, token, core_value_id)
        goal_id = json.loads(goal_response.content)['pk']
        self.token = token
        self.goal_id = goal_id


def create_task(client,
                token,
                goal_id,
                title="Task title",
                description="description",
                is_active=True,
                start_date_time=None,
                repeat_type="Day",
                repeat_period=1,
                selected_week_days=None,
                end_type="Never",
                end_date=None,
                end_after_occurrence=0,
                completely_done=False
                ):
    if not start_date_time:
        start_date_time = datetime.datetime.now()

    data = {
        "title": title,
        "description": description,
        "is_active": is_active,
        "goal": goal_id,
        "start_date_time": start_date_time,
        "repeat_type": repeat_type,
        "repeat_period": repeat_period,
        "selected_week_days": selected_week_days,
        "end_type": end_type,
        "end_date": end_date,
        "end_after_occurrence": end_after_occurrence,
        "completely_done": completely_done
    }
    if not selected_week_days:
        data.pop("selected_week_days")

    if not end_date:
        data.pop("end_date")

    response = client.post(
        '/personal-to-dos/task/',
        data,
        headers={
            'Authorization': token
        }
    )

    return response


def create_partially_completed_task(client,
                                    token,
                                    task_id,
                                    description="description",
                                    is_active=True,
                                    ):
    data = {
        "description": description,
        "is_active": is_active,
        "task": task_id,
    }
    response = client.post(
        '/personal-to-dos/partially-completed-task/',
        data,
        headers={
            'Authorization': token
        }
    )

    return response


class TestTaskAPI(PrepareTaskTestMixin, APITestCase):
    def test_create_task(self):
        task_response = create_task(
            self.client,
            self.token,
            self.goal_id
        )
        self.assertContains(task_response, 'pk', status_code=status.HTTP_201_CREATED)
        task_id = json.loads(task_response.content)['pk']
        task = TaskModel.objects.filter(pk=task_id).first()
        self.assertEqual(task.goal_id, self.goal_id)
        user = UserModel.objects.first()
        self.assertEqual(task.owner, user)

    def test_create_partially_completed_task(self):
        task_response = create_task(
            self.client,
            self.token,
            self.goal_id
        )
        task_id = json.loads(task_response.content)['pk']
        partially_completed_task = create_partially_completed_task(
            self.client,
            self.token,
            task_id,
        )
        self.assertContains(partially_completed_task, "pk", status_code=status.HTTP_201_CREATED)

