
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from rest_framework.exceptions import ValidationError
from .validators import validate_profile_image
from .managers import CustomUserManager
from core.models import TimeStampedModel, CompletedModel, ProgressModel, PriorityModel


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
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
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'O'
    GENDER_NOT_TO_SAY = 'PNS'

    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
        (GENDER_NOT_TO_SAY, 'Prefer not to say'),
    ]

    ASSISTANT_MODEL_CHOICES = [
        ('spouse', 'Spouse'),
        ('friend', 'Friend'),
        ('coach', 'Coach'),
        ('therapist', 'Therapist')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=False)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=False,
                                        validators=[validate_profile_image])
    notification_preferences = models.CharField(max_length=255, default='Push notifications')
    ai_assistant_model = models.CharField(choices=ASSISTANT_MODEL_CHOICES, max_length=255)
    dashboard_customization = models.TextField(blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.user.email} Profile'

    def is_profile_complete(self):
        required_fields = ['birth_date', 'location', 'profile_picture', 'notification_preferences',
                           'user_profile__user_role', 'user_profile__user_goal']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True

    def is_owner(self, user):
        return self.user == user or user.is_staff




class UserRole(models.Model):
    """
    A model representing user roles, either predefined or custom.
    """
    role = models.CharField(max_length=50, blank=True, null=True)
    user_profiles = models.ManyToManyField(UserProfile, related_name='user_roles')
    custom_role = models.CharField(max_length=50, blank=True, null=True, unique=True)
    group_name = models.CharField(max_length=50, blank=True, null=True)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        if self.is_custom:
            return self.custom_role
        return self.role

    def is_owner(self, user):
        return self.user_profiles.filter(user=user).exists() or user.is_staff


class UserGoal(TimeStampedModel, CompletedModel, ProgressModel):
    """
    A model representing goals that users have chosen or created.
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='goals')
    goal = models.ForeignKey('goal_task_management.Goal', on_delete=models.CASCADE, null=True, blank=True)
    custom_goal = models.CharField(max_length=255, blank=True, null=True)
    is_custom = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        user_email = self.user_profile.user.email if self.user_profile else 'No User'
        if self.goal:
            return f'{self.goal.title} ({user_email})'
        return f'{self.custom_goal} ({user_email})'

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user_profile', 'goal'], name='unique_user_goal'),
            UniqueConstraint(fields=['user_profile', 'custom_goal'], name='unique_user_custom_goal'),
        ]

    def clean(self):
        if not self.goal and not self.custom_goal:
            raise ValidationError("Either goal or custom_goal must be set.")
        if self.goal and self.custom_goal:
            raise ValidationError("Both goal and custom_goal cannot be set at the same time.")


class UserTask(TimeStampedModel, CompletedModel, PriorityModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_tasks')
    task = models.ForeignKey('goal_task_management.Task', on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=255, blank=True, null=True)
    progress = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_repetitive = models.BooleanField(default=False)
    repetition_interval = models.CharField(max_length=50, default='daily')
    completion_count = models.IntegerField(default=0)

    def __str__(self):
        return self.custom_name if self.custom_name else self.task.name
