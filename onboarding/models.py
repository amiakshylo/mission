from django.db import models
from django.db.models import UniqueConstraint

from life_sphere.models import LifeSphere
from user_management.models import UserProfile


class OnboardingQuestion(models.Model):
    text = models.TextField()
    life_sphere = models.ForeignKey(
        LifeSphere, on_delete=models.CASCADE, related_name="onboarding_questions"
    )
    order = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Question {self.order}: {self.text}"


class AnswerOption(models.Model):
    question = models.ForeignKey(
        OnboardingQuestion, on_delete=models.CASCADE, related_name="options"
    )
    answer = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    tailored_question = models.ForeignKey(
        "OnboardingQuestion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_question_options",
    )

    def __str__(self):
        return self.answer


class UserResponse(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="responses"
    )
    question = models.ForeignKey(
        OnboardingQuestion, on_delete=models.PROTECT, related_name="user_responses"
    )
    user_answer = models.ForeignKey(
        AnswerOption, on_delete=models.PROTECT, related_name="user_responses"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Response by {self.user_profile.user.username} to '{self.question.text}': {self.user_answer}"

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_profile', 'question'], name='unique_user_question')
        ]
        ordering = ['-timestamp']
