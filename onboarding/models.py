from django.db import models

from user_management.models import UserProfile


class OnboardingStep(models.Model):
    """
    A model representing a step in the onboarding process.
    """
    step_number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'Step {self.step_number}: {self.title}'


class UserOnboardingStatus(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='onboarding_status')
    current_step = models.ForeignKey(OnboardingStep, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Onboarding Status for {self.user_profile.user.email}'
