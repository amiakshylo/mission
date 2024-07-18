from django.db import models
from django.conf import settings
from core.models import TimeStampedModel, CompletedModel, ProgressModel, DueDateModel, StartEndModel, PriorityModel


class Goal(TimeStampedModel, CompletedModel, ProgressModel, DueDateModel, StartEndModel):
    name = models.CharField(max_length=255,  unique=True, blank=False)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_category = models.ForeignKey('category.SubCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Habit(TimeStampedModel, CompletedModel, ProgressModel, StartEndModel):
    name = models.CharField(max_length=255,  unique=True, blank=False)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_category = models.ForeignKey('category.SubCategory', on_delete=models.CASCADE)
    frequency = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class Task(TimeStampedModel, CompletedModel, PriorityModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubTask(TimeStampedModel, CompletedModel, PriorityModel):
    name = models.CharField(max_length=255,  unique=True, blank=False)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
