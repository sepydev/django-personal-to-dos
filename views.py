import os

from django.conf import settings
from django.http.response import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .core_values.views import CoreValueViewSet  # noqa
from .goals.views import GoalViewSet  # noqa
from .tasks.views import TaskViewSet  # noqa


class MedialView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, file):
        full_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, "images/", file)
        response = FileResponse(open(full_path, 'rb'))
        return response
