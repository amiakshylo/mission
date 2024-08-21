from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, CompletedModel, PriorityModel


class Goal(models.Model):
    TYPE_LONG_TERM = 'long_term'  # Long-term goals are goals that take a long time to achieve
    TYPE_SHORT_TERM = 'short_term'  # Short-term goals are goals that can be achieved in a short period of time

    GOAL_TYPE_CHOICES = ((TYPE_SHORT_TERM, 'Short-term'),
                         (TYPE_LONG_TERM, 'Long-term')
                         )

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_custom = models.BooleanField(default=False, null=True)  # Distinguishes predefined from user-created goals
    impact_score = models.IntegerField(null=True, blank=True)
    goal_type = models.CharField(choices=GOAL_TYPE_CHOICES, null=True, blank=True)
    category = models.ManyToManyField('category_management.Category', related_name='goals')
    role = models.ManyToManyField('user_management.Role', related_name='goals')

    def __str__(self):
        return self.title


class Task(TimeStampedModel, CompletedModel, PriorityModel):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    goal = models.ForeignKey('goal_task_management.Goal', on_delete=models.CASCADE, null=True, blank=True)
    habit = models.ForeignKey('habit_management.Habit', on_delete=models.CASCADE, null=True, blank=True)
    is_predefined = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubTask(TimeStampedModel, CompletedModel, PriorityModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='sub_tasks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
