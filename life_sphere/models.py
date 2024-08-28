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
    life_sphere = models.ForeignKey(LifeSphere, on_delete=models.CASCADE, related_name='subcategory')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "SubCategories"


class LifeSphereProgress(ProgressModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(LifeSphere, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user_profile.user} - {self.category.title} - {self.progress}%'

    def is_significantly_engaged(self, threshold=75):
        """Check if the user's progress in the life_sphere meets or exceeds the threshold."""
        return self.progress >= threshold


class LifeSphereCompletion(CompletedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(LifeSphere, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} - {self.category.title}'
