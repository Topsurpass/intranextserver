from django.db import models
import uuid
import random
import string

class TechStack(models.Model):
    """
    Represents the tech stack (e.g., "Back-end, Front-end").
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tech Stack"
        verbose_name_plural = "Tech stacks"


class Course(models.Model):
    """
    Represents a course under a specific tech stack (e.g., "Front-end - Modern Javascript").
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    stack_id = models.ForeignKey(
        TechStack, on_delete=models.CASCADE, related_name='course',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
class Lesson(models.Model):
    """
    Represents a specific Lesson within a course.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')
    title = models.CharField(max_length=255)
    weight = models.IntegerField(default=1)
    level = models.CharField(
        max_length=20,
        choices=[
            ('novice', 'Novice'),
            ('beginner', 'Beginner'),
            ('mid-level', 'Mid-Level'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert')
        ],
        default='novice'
    )
    lesson_code = models.CharField(max_length=4, unique=True, blank=True)  # 4-digit code
    lesson_hex = models.CharField(max_length=4, unique=True, blank=True)  # Hexadecimal code
    deadline_start = models.DateField()
    deadline_end = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.lesson_code:
            self.lesson_code = self.generate_lesson_code()

        if not self.lesson_hex:
            self.lesson_hex = self.generate_lesson_hex()

        super().save(*args, **kwargs)

    def generate_lesson_code(self):
        """Generate a unique 4-digit numeric lesson_code."""
        while True:
            code = f"{random.randint(1000, 9999)}"
            if not Lesson.objects.filter(lesson_code=code).exists():
                return code

    def generate_lesson_hex(self):
        """Generate a unique 6-character hexadecimal lesson_hex."""
        while True:
            hex_code = ''.join(random.choices(string.hexdigits[:16], k=4)).lower()
            if not Lesson.objects.filter(lesson_hex=hex_code).exists():
                return hex_code

    def __str__(self):
        return f"{self.title} ({self.lesson_code})"

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"


class Task(models.Model):
    """
    Represents the tasks in a lesson.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, unique=False)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='tasks')
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"