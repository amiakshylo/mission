from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from user_management.models import UserArea
from .models import LifeSphere, Area
from .pagination import DefaultPagination
from .serializers import LifeSphereSerializer, AreaSerializer, AddUserAreaSerializer


class LifeSphereViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = LifeSphere.objects.all()
    serializer_class = LifeSphereSerializer



class AreaViewSet(ListModelMixin, GenericViewSet):
    queryset = Area.objects.select_related(
            "life_sphere"
        )
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]
    serializer_class = AreaSerializer







