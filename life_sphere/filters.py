import django_filters
from django_filters.rest_framework import FilterSet

from life_sphere.models import Area, LifeSphere


class AreaFilter(FilterSet):


    class Meta:
        model = Area
        fields = ['life_sphere_id']

