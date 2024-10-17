from django.contrib import admin

from . import models


@admin.register(models.LifeSphere)
class LifeSphereAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    search_fields = ["title", "description"]
