from django.urls import path, include
from .views import (
    TaskListView,
    TaskListDetailView,
    TechStackDetailView,
    TechStackListView, 
    LessonListView, 
    LessonDetailView,
    CourseDetailView,
    CourseListView
)
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'task', TaskViewset, basename='task')

urlpatterns = [
    # path('', include(router.urls)),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('task/<uuid:pk>', TaskListDetailView.as_view(), name='task-list'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lesson/<uuid:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('course/<uuid:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('techstacks/', TechStackListView.as_view(), name='techstack-list'),
    path('techstack/<uuid:pk>/', TechStackDetailView.as_view(), name='techstack-detail'),
]

