from django.urls import path, include
from rest_framework import routers

from .views import CoreValueViewSet, GoalViewSet

router = routers.DefaultRouter()
router.register('core-value', CoreValueViewSet)
router.register('goal', GoalViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
