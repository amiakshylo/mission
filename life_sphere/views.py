from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .filters import AreaFilter
from .models import LifeSphere, Area
from .pagination import DefaultPagination
from .serializers import LifeSphereSerializer, AreaSerializer


class LifeSphereViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = LifeSphereSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LifeSphere.objects.all()


class AreaViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = AreaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AreaFilter
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Area.objects.select_related('life_sphere').distinct()
