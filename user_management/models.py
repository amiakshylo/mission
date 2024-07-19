from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from .managers import CustomUserManager


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
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    roles = models.ManyToManyField('Role', related_name='user_profiles')
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} Profile'

    def is_profile_complete(self):
        required_fields = ['birth_date', 'location', 'profile_picture']
        for field in required_fields:
            if not getattr(self, field):
                return False
        return True


ROLE_GROUPS = {
    'Family': [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Husband', 'Husband'),
        ('Wife', 'Wife'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Partner', 'Partner')
    ],
    'Professional': [
        ('Colleague', 'Colleague'),
        ('Mentor', 'Mentor'),
        ('Mentee', 'Mentee'),
        ('Leader', 'Leader'),
        ('Planner', 'Planner'),
        ('Collaborator', 'Collaborator'),
        ('Communicator', 'Communicator'),
        ('Learner', 'Learner'),
    ],
    'Other': [
        ('Friend', 'Friend'),
        ('Other', 'Other'),
    ]
}


ROLE_CHOICES = [(role, name) for group in ROLE_GROUPS.values() for role, name in group]


class Role(models.Model):
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES)
    role_group = models.CharField(max_length=50, choices=[(group, group) for group in ROLE_GROUPS.keys()])
    custom_role_name = models.CharField(max_length=25, blank=True, null=True)
    is_custom = models.BooleanField(default=False)

    def clean(self):
        # Validation to ensure custom_role_name does not match any predefined role_name
        if self.custom_role_name:
            predefined_role_names = [choice[0] for choice in ROLE_CHOICES]
            if self.custom_role_name in predefined_role_names:
                raise ValidationError({'custom_role_name': 'This role already exists as a predefined role.'})

    def save(self, *args, **kwargs):
        self.clean()
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.custom_role_name if self.is_custom else self.role_name
