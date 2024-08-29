from django.db import models


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
    ]
    response = models.IntegerField(choices=RESPONSE_CHOICES)

    def __str__(self):
        return f"{self.user_profile.user} - {self.question.text} - {self.get_response_display()}"
