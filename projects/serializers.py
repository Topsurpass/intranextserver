from rest_framework import serializers
from .models import TechStack, Course, Lesson, Task


class LessonTaskSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Lesson
        fields = ('title',) 
class TaskSerializer(serializers.ModelSerializer):
    lesson_id = LessonTaskSerializer(read_only=True)
    class Meta:
        model = Task
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    # The Task model is related to Lesson using related_name='tasks'
    tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Lesson
        fields = '__all__'

    def get_tasks(self, obj):
        """Return tasks ordered by created_at in ascending order."""
        tasks = obj.tasks.all().order_by('created_at')
        return TaskSerializer(tasks, many=True).data

class CourseSerializer(serializers.ModelSerializer):
    # The Lesson model is related to Course using related_name='lesson'
    lesson = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'

class TechStackSerializer(serializers.ModelSerializer):
    # The Course model is related to TechStack using related_name='course'
    course = CourseSerializer(many=True, read_only=True)
    
    class Meta:
        model = TechStack
        fields = '__all__'
