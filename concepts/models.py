from django.db import models
import uuid
from projects.models import Lesson


class Concept(models.Model):
    """
    Represents the tech stack (e.g., "Back-end, Front-end").
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField(blank=True, null=True)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='concept')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = "Concept"
        verbose_name_plural = "Concepts"