from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, CompletedModel, PriorityModel
from user_management.models import UserProfile, Role


class Goal(TimeStampedModel):
    TYPE_LONG_TERM = (
        "long_term"  # Long-term goals are goals that take a long time to achieve
    )
    TYPE_SHORT_TERM = "short_term"  # Short-term goals are goals that can be achieved in a short period of time

    GOAL_TYPE_CHOICES = ((TYPE_SHORT_TERM, "Short-term"), (TYPE_LONG_TERM, "Long-term"))

    title = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    is_custom = models.BooleanField(default=False, null=True)
    impact_score = models.IntegerField(null=True, blank=True)
    goal_type = models.CharField(choices=GOAL_TYPE_CHOICES, null=True, blank=True)
    area = models.ManyToManyField("life_sphere.Area", related_name="goals")
    role = models.ManyToManyField("user_management.Role", related_name="goals")
    hash = models.CharField(max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title


class GoalSuggestionLog(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="suggestions"
    )
    goal = models.ForeignKey(
        "goal_task.Goal", on_delete=models.CASCADE, null=True, blank=True
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    suggestion_source = models.CharField(max_length=255)  # 'ai' or 'ml_model'
    suggested_at = models.DateTimeField(auto_now_add=True)
    user_feedback = models.CharField(
        max_length=255, null=True, blank=True
    )  # optional feedback from user

    def __str__(self):
        return f"Suggestion for {self.user_profile.user.email} from {self.suggestion_source}"


class Task(TimeStampedModel, CompletedModel, PriorityModel):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    goal = models.ForeignKey(
        "goal_task.Goal", on_delete=models.CASCADE, null=True, blank=True
    )
    is_predefined = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubTask(TimeStampedModel, CompletedModel, PriorityModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="sub_tasks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
