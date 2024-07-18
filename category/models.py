from django.db import models
from django.conf import settings
from core.models import TimeStampedModel, ProgressModel, CompletedModel


class MainCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class SubCategory(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField()
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserCategoryProgress(ProgressModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f'{self.user.name} - {self.category.name} - {self.progress}%'

    def is_significantly_engaged(self, threshold=75):
        """Check if the user's progress in the category meets or exceeds the threshold."""
        return self.progress >= threshold


class MainCategoryCompletion(CompletedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} - {self.main_category.name}'


class SubCategoryCompletion(CompletedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name} - {self.sub_category.name}'
