from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


def validate_start_due_date(value):
    if value < timezone.now().date():
        raise ValidationError("Start/due date cannot be in the past.")


class StartEndModel(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class CompletedModel(models.Model):
    completed_at = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)

    class Meta:
        abstract = True



class ProgressModel(models.Model):
    progress = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0),
        ],
        help_text="Progress in percentage",
    )

    class Meta:
        abstract = True



class DueDateModel(models.Model):
    due_date = models.DateField(
        validators=[validate_start_due_date], null=True, blank=True
    )

    class Meta:
        abstract = True


class PriorityModel(models.Model):
    PRIORITY_CHOICES = [("L", "Low"), ("M", "Medium"), ("H", "High"), ("C", "Critical")]
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default="M")

    class Meta:
        abstract = True
