from django.urls import path, include
from rest_framework import routers

from .views import CoreValueViewSet, \
    GoalViewSet, \
    MedialView, \
    TaskViewSet, \
    PartiallyCompletedTaskViewSet, \
    TodoAPIView

router = routers.DefaultRouter()
router.register('core-value', CoreValueViewSet)
router.register('goal', GoalViewSet)
router.register('task', TaskViewSet)
router.register('partially-completed-task', PartiallyCompletedTaskViewSet)
router.register('to-do-list', TodoAPIView)


urlpatterns = [
    path('', include(router.urls)),
    path('media/images/<str:file>', MedialView.as_view(), name='images'),

]
