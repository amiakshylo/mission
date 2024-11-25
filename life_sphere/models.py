from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, ProgressModel, CompletedModel
from user_management.models import UserProfile


class LifeSphere(models.Model):
    """
    A model representing life spheres.
    """

    title = models.CharField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Area(models.Model):
    """
    A model representing an areas of interest.
    """

    title = models.CharField()
    description = models.TextField(blank=True, null=True)
    life_sphere = models.ForeignKey(
        LifeSphere, on_delete=models.CASCADE, related_name="areas"
    )

    def __str__(self):
        return self.title
