from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from seven import settings
from user_management.models import UserProfile, Role


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


@receiver(post_migrate)
def add_predefined_roles(sender, **kwargs):
    if sender.name == 'user_management':
        for group, roles in Role.ROLE_GROUPS.items():
            for role_name, role_display in roles:
                Role.objects.get_or_create(role_name=role_name, role_group=group)
