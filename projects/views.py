from .models import Task, TechStack, Lesson, Course
from .serializers import TaskSerializer, LessonSerializer, CourseSerializer
from rest_framework import viewsets, generics
# from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import TechStackSerializer


class TechStackListView(generics.ListAPIView):
    """
    Returns a list of all TechStacks with nested Courses, Lessons, and Tasks.
    """
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer

class TechStackDetailView(generics.RetrieveAPIView):
    """
    Returns a single TechStack with its nested data.
    """
    queryset = TechStack.objects.all()
    serializer_class = TechStackSerializer
class CourseListView(generics.ListAPIView):
    """
    Returns all Courses with its nested data.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(generics.RetrieveAPIView):
    """
    Returns a single course with its nested data.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class LessonListView(generics.ListAPIView):
    """Returns List of all lessons."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDetailView(generics.RetrieveAPIView):
    """Returns a single lesson."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class TaskListView(generics.ListAPIView):
    """List all tasks."""
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
class TaskListDetailView(generics.RetrieveAPIView):
    """Returns a single task."""
    serializer_class = TaskSerializer
    queryset = Task.objects.all()