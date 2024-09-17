from django_filters.rest_framework import FilterSet

from user_management.models import Role


class RoleFilter(FilterSet):
    class Meta:
        model = Role
        fields = {"type": ["exact"]}
