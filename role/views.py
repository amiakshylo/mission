from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from user_management.filters import RoleFilter
from user_management.models import Role
from user_management.pagination import DefaultPagination
from user_management.serializers import RoleSerializer


class RoleViewSet(ListModelMixin, GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RoleFilter
    search_fields = ["title"]
