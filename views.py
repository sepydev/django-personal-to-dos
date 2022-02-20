from .core_values.views import CoreValueViewSet  # noqa
from .goals.views import GoalViewSet  # noqa

from django.conf import settings
import os
from django.http.response import FileResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class MedialView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, file):
        full_path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, "images/", file)
        response = FileResponse(open(full_path, 'rb'))
        return response
