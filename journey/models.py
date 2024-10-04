from django.db import models
from django.utils import timezone
from user_management.models import UserProfile
from core.models import ProgressModel, StartEndModel, CompletedModel


class Journey(models.Model):
    """
    A model representing a journey.
    """

    title = models.CharField(max_length=255)
    journey_number = models.PositiveIntegerField(unique=True)
    description = models.TextField()

    def __str__(self):
        return f"Journey {self.journey_number}: {self.title}"

    class Meta:
        ordering = ['journey_number']



class JourneyStep(models.Model):
    """
    A model representing a step in a journey.
    """

    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name="steps")

    title = models.CharField(max_length=255)
    step_number = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['step_number']
        unique_together = ('journey', 'step_number')


class UserJourneyStepStatus(CompletedModel, StartEndModel):
    """
    A model representing the status of a user completing a journey step.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="step_statuses"
    )
    step = models.ForeignKey(
        JourneyStep, on_delete=models.CASCADE, related_name="step_statuses"
    )
    paused = None
    ended_at = None


class UserJourneyStatus(StartEndModel, CompletedModel):
    """
    A model representing the status of a user's journey.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="journey_statuses"
    )
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='statuses')
    current_step = models.ForeignKey(JourneyStep, on_delete=models.CASCADE)
    completed_steps = models.IntegerField(default=0)
    paused = None
    ended_at = None

    def __str__(self):
        return f"{self.user_profile.name} - {self.journey.title} - {'Completed' if self.is_completed else 'Active'}"

    class Meta:
        unique_together = ('user_profile', 'journey')
