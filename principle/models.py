from django.contrib.postgres.indexes import GinIndex
from django.db import models

from core.model_choices import GenderChoices


class Principle(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey("user_management.UserProfile", on_delete=models.DO_NOTHING)
    is_predefined = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class RoleModel(models.Model):
    character_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255)
    principle = models.ManyToManyField(Principle, related_name='rolemodels')
    gender = models.CharField(choices=GenderChoices.GENDER_TYPE_CHOICES)

    class Meta:
        indexes = [
            GinIndex(
                name='rolemodel_name_trigram',
                fields=['character_name'],
                opclasses=['gin_trgm_ops']
            )
        ]
