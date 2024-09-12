from django.db import models

from life_sphere.models import LifeSphere
from user_management.models import UserProfile


class OnboardingQuestion(models.Model):
    text = models.TextField()
    life_sphere = models.ForeignKey('life_sphere.LifeSphere', on_delete=models.CASCADE, related_name="questions")
    is_followup = models.BooleanField(default=False)
    followup_condition = models.ForeignKey('AnswerOption', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text


class AnswerOption(models.Model):
    question = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE, related_name="options")
    option = models.CharField(max_length=255)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.option


class OnboardingAnswer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE)
    user_answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user_profile} - {self.question} - {self.user_answer}"


class OnboardingProgress(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    current_life_sphere = models.ForeignKey(LifeSphere, on_delete=models.SET_NULL, null=True)
    completed_questions = models.ManyToManyField(OnboardingQuestion, related_name='completed_by_users')
    skipped_questions = models.ManyToManyField(OnboardingQuestion, related_name='skipped_by_users')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile} - Current Sphere: {self.current_life_sphere}"
