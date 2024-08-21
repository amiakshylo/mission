from django.contrib import admin

from user_management import models



@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user']




@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'category']
    autocomplete_fields = ['category']
    search_fields = ['title', 'description']

    def get_queryset(self, request):
        return models.Role.objects.select_related('category').all()
