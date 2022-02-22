from django.urls import path, include
from rest_framework import routers

from .views import CoreValueViewSet, GoalViewSet, MedialView, TaskViewSet

router = routers.DefaultRouter()
router.register('core-value', CoreValueViewSet)
router.register('goal', GoalViewSet)
router.register('task', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('media/images/<str:file>', MedialView.as_view(), name='images'),

]
