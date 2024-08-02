from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, CompletedModel, ProgressModel, StartEndModel
from user_management.models import UserProfile


class Habit(TimeStampedModel, ProgressModel, StartEndModel):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_habits')
    sub_category = models.ForeignKey('category_management.SubCategory', on_delete=models.CASCADE)
    frequency = models.JSONField(default=dict)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'user_profile'], name='unique_habit_per_user'),
        ]
