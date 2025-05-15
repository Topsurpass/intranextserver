from django.contrib import admin
from .models import TechStack, Course, Lesson, Task

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'stack_id', 'start_date', 'end_date')
    list_filter = ('stack_id',)

@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_id', 'level', 'lesson_code', 'lesson_hex', 'deadline_start', 'deadline_end')
    list_filter = ('course_id',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_id', 'created_at')
    list_filter = ('lesson_id',)
