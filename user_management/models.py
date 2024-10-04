from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError

from core.model_choices import (
    GoalTypeChoices,
    RoleChoices,
    UserProfileChoices,
)
from core.models import (
    TimeStampedModel,
    CompletedModel,
    ProgressModel,
    PriorityModel,
    DueDateModel,
)
from principle_management.models import Principle
from .managers import CustomUserManager
from .validators import validate_profile_image


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    def get_full_name_or_email(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email


class UserProfile(models.Model):
    """
    A model representing additional profile information for the user.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r"^[A-Za-z ]+$",
                message="Name must contain only letters and spaces.",
                code="invalid_name",
            ),
        ],
    )
    gender = models.CharField(
        max_length=20, choices=UserProfileChoices.GENDER_CHOICES, blank=False
    )
    custom_gender = models.CharField(
        max_length=50,
        blank=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r"^[A-Za-z ]+$",
                message="Custom gender must contain only letters and spaces.",
                code="invalid_gender",
            ),
        ],
    )
    profile_image = models.ImageField(
        upload_to="profile_picture/",
        blank=True,
        null=False,
        validators=[validate_profile_image],
    )
    birth_date = models.DateField(null=True, blank=False)
    age_range = models.IntegerField(
        choices=UserProfileChoices.AGE_RANGE_CHOICES,
        default=UserProfileChoices.AGE_RANGE_PREFER_NOT_TO_SAY,
    )
    notification_preferences = models.CharField(
        max_length=255, default="Push notifications"
    )
    ai_assistant_model = models.CharField(
        choices=UserProfileChoices.ASSISTANT_MODEL_CHOICES, max_length=255
    )
    dashboard_customization = models.TextField(blank=True)

    def get_age(self):
        if self.birth_date:
            today = date.today()
            return (
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
        return

    def __str__(self):
        if self.custom_gender:
            return self.custom_gender
        return self.gender

    def is_profile_complete(self):
        required_fields = [
            "birth_date",
            "location",
            "profile_picture",
            "notification_preferences",
            "user_profile__user_role",
            "user_profile__user_goal",
        ]
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True

    def save(self, *args, **kwargs):
        custom_gender = self.custom_gender
        if custom_gender:
            self.gender = custom_gender

        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        unique_together = ["user", "profile_image"]


class UserArea(TimeStampedModel):
    """
    A model representing the area of interest of the user
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_areas"
    )
    area = models.ForeignKey("life_sphere.Area", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.area.title


class UserMission(TimeStampedModel):
    """
    A model representing the mission statement of the user.
    """

    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="user_missions"
    )
    mission_statement = models.TextField(blank=True)
    tailored_by_ai = models.BooleanField(
        default=False
    )  # Indicates if the mission was tailored by AI
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Mission for {self.user_profile.user.email}"


class Role(TimeStampedModel):
    """
    A model representing user roles, either predefined or custom.
    """

    title = models.CharField(max_length=50, unique=True, blank=True)
    type = models.CharField(max_length=50, choices=RoleChoices.ROLE_TYPE_CHOICES)
    description = models.TextField(blank=True)
    user_profile = models.ManyToManyField(UserProfile, related_name="roles")
    custom_title = models.CharField(
        max_length=50, unique=True, null=True, blank=True, default="Default Title"
    )
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class UserGoal(TimeStampedModel, CompletedModel, ProgressModel, DueDateModel):
    """
    A model representing goals that users have chosen or created.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="goals"
    )
    goal = models.ForeignKey(
        "goal_task_management.Goal", on_delete=models.CASCADE, blank=True
    )
    custom_goal = models.CharField(max_length=255, blank=True)
    goal_type = models.CharField(choices=GoalTypeChoices.GOAL_TYPE_CHOICES)
    is_custom = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        user_email = self.user_profile.user.email if self.user_profile else "No User"
        if self.goal:
            return f"{self.goal.title} ({user_email})"
        return f"{self.custom_goal} ({user_email})"

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user_profile", "goal"], name="unique_user_goal"),
            UniqueConstraint(
                fields=["user_profile", "custom_goal"], name="unique_user_custom_goal"
            ),
        ]

    def clean(self):
        if not self.goal and not self.custom_goal:
            raise ValidationError("Either goal or custom_goal must be set.")
        if self.goal and self.custom_goal:
            raise ValidationError(
                "Both goal and custom_goal cannot be set at the same time."
            )

    def save(self, *args, **kwargs):
        if self.is_completed:
            self.is_active = False
        else:
            self.is_active = True
        super().save(*args, **kwargs)


class UserTask(TimeStampedModel, CompletedModel, PriorityModel):
    """
    A model representing tasks that users have chosen or created.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_tasks"
    )
    task = models.ForeignKey("goal_task_management.Task", on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=255, blank=True)
    progress = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_repetitive = models.BooleanField(default=False)
    repetition_interval = models.CharField(max_length=50, default="daily")
    completion_count = models.IntegerField(default=0)

    def __str__(self):
        return self.custom_name if self.custom_name else self.task.name


class UserPrinciple(TimeStampedModel):
    """
    A model representing the principles that users have chosen or created.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_principles"
    )
    principle = models.ForeignKey(
        Principle, on_delete=models.CASCADE, null=True, blank=True
    )
    custom_principle = models.CharField(max_length=255, blank=True)
    is_custom = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        user_email = self.user_profile.user.email if self.user_profile else "No User"
        if self.principle:
            return f"{self.principle.title} ({user_email})"
        return f"{self.custom_principle} ({user_email})"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user_profile", "principle"], name="unique_user_principle"
            ),
            UniqueConstraint(
                fields=["user_profile", "custom_principle"],
                name="unique_user_custom_principle",
            ),
        ]

    def clean(self):
        if not self.principle and not self.custom_principle:
            raise ValidationError("Either principle or custom_principle must be set.")
        if self.principle and self.custom_principle:
            raise ValidationError(
                "Both principle and custom_principle cannot be set at the same time."
            )


class UserBalance(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="balances"
    )
    life_sphere = models.ForeignKey(
        "life_sphere.LifeSphere", on_delete=models.CASCADE, related_name="user_balances"
    )
    score = models.IntegerField()

    def __str__(self):
        return f"{self.user_profile} - {self.life_sphere.title}: {self.score}"
