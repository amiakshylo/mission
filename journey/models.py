from django.db import models

from user_management.models import UserProfile


class Journey(models.Model):
    """
    A model representing a journey.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class JourneyStep(models.Model):
    """
    A model representing a step in a journey.
    """
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class UserJourneyStatus(models.Model):
    """
    A model representing the status of a user's journey.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='journey_statuses')
    current_step = models.ForeignKey(JourneyStep, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.current_step.title}"
