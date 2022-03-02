import os

from django.conf import settings
from django.http.response import FileResponse
from rest_framework.permissions import IsAuthenticated

from core.views import APIView
from helpers.swagger import APIViewTagDecorator
from .core_values.views import CoreValueViewSet  # noqa
from .goals.views import GoalViewSet  # noqa
from .tasks.views import TaskViewSet, PartiallyCompletedTaskViewSet  # noqa
from .to_dos.views import TodoAPIView  # noqa


@APIViewTagDecorator(methods=('get',), tags=("Media",))
class MedialView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, file):
        full_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, "images/", file)
        response = FileResponse(open(full_path, 'rb'))
        return response
