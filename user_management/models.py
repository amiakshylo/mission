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
from goal_task.models import Goal
from principle.models import Principle
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


class UserProfile(models.Model):
    """
    A model representing additional profile information for the user.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    name = models.CharField(
        max_length=50,
        blank=True,
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
        max_length=20,
        choices=UserProfileChoices.GENDER_CHOICES,
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
    age_range = models.IntegerField(null=True)

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
        return self.name.strip() if self.name else "Unnamed User Profile"

    def is_profile_complete(self):
        required_fields = [
            "birth_date",
            "profile_picture",
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
    tailored_by_ai = models.BooleanField(default=False)
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
        "goal_task.Goal", on_delete=models.CASCADE, blank=True
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

    @classmethod
    def create_user_goal(cls, user_profile, validated_data):
        custom_goal_title = validated_data.get("custom_goal")
        goal = validated_data.get("goal")

        if custom_goal_title:
            goal = Goal.objects.create(
                title=custom_goal_title,
                description=custom_goal_title,
                goal_type=validated_data.get('goal_type'),
                is_custom=True,
                created_by=user_profile.id
            )

        return cls.objects.create(
            user_profile=user_profile,
            goal=goal,
            goal_type=validated_data.get("goal_type"),
            due_date=validated_data.get("due_date")
        )


class UserTask(TimeStampedModel, CompletedModel, PriorityModel):
    """
    A model representing tasks that users have chosen or created.
    """

    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="user_tasks"
    )
    task = models.ForeignKey("goal_task.Task", on_delete=models.CASCADE)
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
        UserProfile, on_delete=models.CASCADE, related_name="principles"
    )
    principle = models.ForeignKey(
        Principle, on_delete=models.DO_NOTHING, blank=True
    )

    def __str__(self):
        return self.principle

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["user_profile", "principle"], name="unique_user_principle"
            )
        ]


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
