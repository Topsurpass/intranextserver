import nested_admin
from django.contrib import admin
from .models import TechStack, Course, Lesson, Task
from concepts.models import Concept


class ConceptInline(nested_admin.NestedTabularInline):
    model = Concept
    extra = 1


class TaskInline(nested_admin.NestedTabularInline):
    model = Task
    extra = 1


class LessonInline(nested_admin.NestedStackedInline):
    model = Lesson
    extra = 1
    inlines = [ConceptInline, TaskInline]


@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'stack_id', 'start_date', 'end_date')
    list_filter = ('stack_id',)
    inlines = [LessonInline]


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')

