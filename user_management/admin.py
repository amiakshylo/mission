from django.contrib import admin
from user_management import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name']


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

