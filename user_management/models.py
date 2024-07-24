import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError
from .validators import validate_profile_image
from .managers import CustomUserManager
from core.models import TimeStampedModel


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
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True,
                                        validators=[validate_profile_image])
    current_habits = models.TextField(blank=True, null=True)
    notification_preferences = models.CharField(max_length=255, default='Push notifications')
    ai_assistant_model = models.CharField(choices=ASSISTANT_MODEL_CHOICES, max_length=255)
    dashboard_customization = models.TextField(blank=True, null=True)
    roles = models.ManyToManyField('UserRole', blank=True)
    goals = models.ManyToManyField('UserGoal', blank=True)

    def __str__(self):
        return f'{self.user.email} Profile'

    def clean(self):
        super().clean()
        if self.birth_date:
            if not isinstance(self.birth_date, datetime.date):
                raise ValidationError("Birth date must be a valid date in YYYY-MM-DD format.")
            if self.birth_date > datetime.date.today():
                raise ValidationError("Birth date cannot be in the future.")

    def is_profile_complete(self):
        required_fields = ['birth_date', 'location', 'profile_picture']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True


class PredefinedRole(models.Model):
    """
    A model representing predefined roles that users can choose from.
    """
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    group = models.CharField(max_length=50, choices=[('Family', 'Family'), ('Professional', 'Professional'), ('Personal', 'Personal')])
    goal = models.ManyToManyField('PredefinedGoal', related_name='roles')

    def __str__(self):
        return self.title



class PredefinedGoal(models.Model):
    """
    A model representing predefined goals that users can choose from.
    """
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50,choices=[('Personal', 'Personal'), ('Professional', 'Professional')])
    role = models.ManyToManyField('PredefinedRole', related_name='goals')

    def __str__(self):
        return f'{self.title} ({self.type})'


class UserRole(models.Model):
    """
    A model representing user roles, either predefined or custom.
    """
    predefined_role = models.ForeignKey(PredefinedRole, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='user_roles')
    custom_title = models.CharField(max_length=50, blank=True, null=True)
    custom_group = models.CharField(max_length=50, blank=True, null=True)
    is_custom = models.BooleanField(default=False)


    def __str__(self):
        if self.is_custom:
            return self.custom_title
        return self.predefined_role.title if self.predefined_role else 'Custom Role'


class UserGoal(models.Model):
    """
    A model representing goals that users have chosen or created.
    """
    predefined_goal = models.ForeignKey(PredefinedGoal, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='user_goals')
    custom_title = models.CharField(max_length=255, blank=True, null=True)
    custom_description = models.TextField(blank=True, null=True)
    is_initial = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        if self.predefined_goal:
            return f'{self.predefined_goal.title} ({self.user.email})'
        return f'{self.custom_title} ({self.user.email})'


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
    """
    A model representing the user's progress through the onboarding process.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='onboarding_status')
    current_step = models.ForeignKey(OnboardingStep, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'Onboarding Status for {self.user.email}'


class UserSatisfaction(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('health', 'Health'),
        ('finance', 'Finance'),
        ('relationships', 'Relationships'),
        ('mental_health', 'Mental Health'),
        ('career', 'Career'),
        ('personal_development', 'Personal Development'),
    ]
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='satisfaction_scores')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    score = models.PositiveIntegerField(default=5)

    class Meta:
        unique_together = ('user_profile', 'category')

    def __str__(self):
        return f'{self.user_profile.user.email} - {self.category} Satisfaction'
