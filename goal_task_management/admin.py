from django.contrib import admin

from . import models


@admin.register(models.Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_filter = ['role']






