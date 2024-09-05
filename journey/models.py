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


class JourneyStep(StartEndModel):
    """
    A model representing a step in a journey.
    """
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class UserJourneyStepStatus(models.Model):
    """
    A model representing the status of a user completing a journey step.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='step_statuses')
    step = models.ForeignKey(JourneyStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def mark_completed(self):
        """Marks a step as completed."""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()


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

    def update_progress(self):
        """
        Update progress based on the completed steps and total steps in the journey.
        Ensure the journey is only completed when all steps are done.
        """
        total_steps = self.journey.steps.count()
        completed_steps = UserJourneyStepStatus.objects.filter(
            user_profile=self.user_profile,
            step__journey=self.journey,
            is_completed=True
        ).count()

        # Update progress percentage
        self.progress = (completed_steps / total_steps) * 100

        # Mark journey as completed if all steps are done
        if completed_steps == total_steps:
            self.is_completed = True
            self.completed_at = timezone.now()

        self.save()
