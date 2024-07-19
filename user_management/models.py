from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from .managers import CustomUserManager
from .data import role_choises


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name_or_email(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    roles = models.ManyToManyField('Role', related_name='user_profiles')
    goal = models.ManyToManyField('Goal', related_name='user_profiles')
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} Profile'

    def is_profile_complete(self):
        required_fields = ['birth_date', 'location', 'profile_picture']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True


class Role(models.Model):
    role_name = models.CharField(max_length=50)
    role_group = models.CharField(max_length=50)
    custom_role_name = models.CharField(max_length=25, blank=True, null=True)
    is_custom = models.BooleanField(default=False)

    def clean(self):
        # Validation to ensure custom_role_name does not match any predefined role_name
        if self.custom_role_name:
            predefined_role_names = [choice[0] for choice in role_choises.ROLE_CHOICES]
            if self.custom_role_name in predefined_role_names:
                raise ValidationError({'custom_role_name': 'This role already exists in our data.'})

    def save(self, *args, **kwargs):
        self.clean()
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.custom_role_name if self.is_custom else self.role_name


class Goal(models.Model):
    PERSONAL = 'Personal'
    PROFESSIONAL = 'Professional'

    GOAL_TYPES = [
        (PERSONAL, 'Personal'),
        (PROFESSIONAL, 'Professional'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)

    def __str__(self):
        return f'{self.title} ({self.goal_type})'
