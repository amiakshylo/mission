from django.contrib import admin

from user_management import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]
    search_fields = ['email']

    list_per_page = 10


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_per_page = 10


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]
    list_per_page = 10

    search_fields = ["title", "description"]

    def get_queryset(self, request):
        return models.Role.objects.all()
