import nested_admin
from django.contrib import admin
from .models import Exam, Question, Option, ExamSubmission


class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 2


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [OptionInline]
    extra = 1
    show_change_link = True


@admin.register(Exam)
class ExamAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam')
    list_filter = ('exam',)
    search_fields = ('text',)
    # Optional: If you still want to edit Question separately
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question',)
    search_fields = ('text', 'question__text')


@admin.register(ExamSubmission)
class ExamSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'score', 'submitted_at')
    list_filter = ('exam',)
    search_fields = ('user__email', 'exam__title')
