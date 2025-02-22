from django.urls import path, include
from .views import TaskViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'task', TaskViewset, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]

