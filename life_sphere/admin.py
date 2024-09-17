from django.contrib import admin

from . import models


@admin.register(models.LifeSphere)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    search_fields = ["title", "description"]
