from django.db import models

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
    question = models.ForeignKey(OnboardingQuestion, on_delete=models.CASCADE)
    user_answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile} - {self.question} - {self.user_answer}"

    class Meta:
        unique_together = ("user_profile", "question")


class OnboardingProgress(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    completed_questions = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def calculate_remaining_questions(self):
        questions_remain = 13 - self.completed_questions
        return questions_remain
