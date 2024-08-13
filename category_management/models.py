from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, ProgressModel, CompletedModel
from user_management.models import UserProfile


class MainCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name




class UserCategoryProgress(ProgressModel):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user_profile.user} - {self.main_category.name} - {self.progress}%'

    def is_significantly_engaged(self, threshold=75):
        """Check if the user's progress in the category_management meets or exceeds the threshold."""
        return self.progress >= threshold


class MainCategoryCompletion(CompletedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} - {self.main_category.name}'


