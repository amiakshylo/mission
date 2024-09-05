from django.db import models
from django.utils import timezone
from user_management.models import UserProfile
from core.models import ProgressModel, StartEndModel, CompletedModel


class Journey(models.Model):
    """
    A model representing a journey.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class JourneyStep(models.Model):
    """
    A model representing a step in a journey.
    """
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class UserJourneyStepStatus(CompletedModel, StartEndModel):
    """
    A model representing the status of a user completing a journey step.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='step_statuses')
    step = models.ForeignKey(JourneyStep, on_delete=models.CASCADE, related_name='step_statuses')
    paused = None
    ended_at = None






class UserJourneyStatus(ProgressModel, StartEndModel, CompletedModel):
    """
    A model representing the status of a user's journey.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='journey_statuses')
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, null=True)
    current_step = models.ForeignKey(JourneyStep, on_delete=models.CASCADE)
    paused = None

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.journey.title} - {self.current_step.title}"


