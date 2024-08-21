from django.conf import settings
from django.db import models


class Principle(models.Model):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_predefined = models.BooleanField(default=False)

    def __str__(self):
        return self.title
