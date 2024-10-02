from django_filters import filters
from django_filters.rest_framework import FilterSet

from user_management.models import Role, UserArea


class RoleFilter(FilterSet):
    class Meta:
        model = Role
        fields = {"type": ["exact"]}


class UserAreaFilter(FilterSet):
    life_sphere = filters.NumberFilter(
        field_name="area__life_sphere__title",
        lookup_expr="exact",
        label="Life Sphere",
        help_text="Filter by Area Life Sphere ID",
    )

    class Meta:
        model = UserArea
        fields = ["life_sphere", "is_active"]
