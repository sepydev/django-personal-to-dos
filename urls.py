from django.urls import path, include
from rest_framework import routers

from .views import CoreValueViewSet

router = routers.DefaultRouter()
router.register('core-value', CoreValueViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
