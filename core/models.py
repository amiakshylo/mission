from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def validate_start_due_date(value):
    if value < timezone.now().date():
        raise ValidationError('Start/due date cannot be in the past.')


class StartEndModel(models.Model):
    start_date = models.DateTimeField(validators=[validate_start_due_date])
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class CompletedModel(models.Model):
    completed_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def update_status_to_complete(self):
        """Mark the item as complete if it's not already."""
        if not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save(update_fields=['completes', 'completed_at'])

    def calculate_duration(self):
        """Calculate the duration from item creation to completion."""
        if self.completed and self.completed_at:
            duration = self.completed_at - self.created_at
            return duration.total_seconds() / 3600
        return None


class ProgressModel(models.Model):
    progress = models.FloatField(default=0.0, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(100.0)
    ])

    class Meta:
        abstract = True


class DueDateModel(models.Model):
    due_date = models.DateTimeField(validators=[validate_start_due_date])

    class Meta:
        abstract = True


class PriorityModel(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('C', 'Critical')
    ]
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')

    class Meta:
        abstract = True