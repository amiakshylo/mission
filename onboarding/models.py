from django.db import models

from life_sphere.models import LifeSphere
from user_management.models import UserProfile


class OnboardingQuestion(models.Model):
    text = models.TextField()
    life_sphere = models.ForeignKey('life_sphere.LifeSphere', on_delete=models.CASCADE, related_name="questions")


    def __str__(self):
        return self.text


class OnboardingResponse(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE, related_name="responses")
    RESPONSE_CHOICES = [
        (10, "Strongly Agree"),
        (5, "Agree"),
        (-5, "Disagree"),
        (-10, "Strongly Disagree"),
        (0, "I don't know"),
    ]
    response = models.IntegerField(choices=RESPONSE_CHOICES)

    def __str__(self):
        return f"{self.user_profile.user} - {self.question.text} - {self.get_response_display()}"


class UserProgress(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    current_life_sphere = models.ForeignKey(LifeSphere, on_delete=models.SET_NULL, null=True)
    completed_questions = models.ManyToManyField(OnboardingQuestion, related_name='completed_by_users')
    skipped_questions = models.ManyToManyField(OnboardingQuestion, related_name='skipped_by_users')
