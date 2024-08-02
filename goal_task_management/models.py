from django.db import models
from django.conf import settings
from core.models import TimeStampedModel, CompletedModel, PriorityModel


class Goal(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey('category_management.SubCategory', on_delete=models.CASCADE)
    is_predefined = models.BooleanField(default=True, null=True, blank=True)
    impact_score = models.IntegerField(null=True, blank=True)
    goal_type = models.CharField(max_length=255, blank=False, null=True)
    user_role = models.ManyToManyField('user_management.UserRole', related_name='goals')

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
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
