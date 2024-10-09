from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from principle_management.filters import TrigramSimilaritySearchFilter
from principle_management.models import RoleModel
from principle_management.serializers import RoleModelSerializer


class RoleModelViewSet(ListModelMixin, GenericViewSet):
    queryset = RoleModel.objects.prefetch_related("principle").all()
    serializer_class = RoleModelSerializer
    filter_backends = [DjangoFilterBackend, TrigramSimilaritySearchFilter]
    search_fields = ['character_name']
