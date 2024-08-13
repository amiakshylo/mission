from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, CompletedModel, ProgressModel, StartEndModel
from user_management.models import UserProfile


class Habit(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    # sub_category = models.ForeignKey('category_management.SubCategory', on_delete=models.CASCADE)
    frequency = models.JSONField(default=dict, null=True, blank=True)
    is_predefined = models.BooleanField(default=False)  # Distinguishes predefined from user-created habits

    def __str__(self):
        return self.title
