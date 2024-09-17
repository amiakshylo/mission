from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from user_management.models import UserArea
from .filters import AreaFilter
from .models import LifeSphere, Area
from .pagination import DefaultPagination
from .serializers import LifeSphereSerializer, AreaSerializer, AddUserAreaSerializer


class LifeSphereViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = LifeSphere.objects.all()
    serializer_class = LifeSphereSerializer
    permission_classes = [IsAuthenticated]


class AreaViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination
    filter_backends = [SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        life_sphere_pk = self.kwargs.get("life_sphere_pk")
        return Area.objects.filter(life_sphere_id=life_sphere_pk).select_related(
            "life_sphere"
        )

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return AddUserAreaSerializer
        return AreaSerializer

    def update(self, request, *args, **kwargs):
        user_profile = request.user.user_profile
        area = self.get_object()
        user_area, created = UserArea.objects.get_or_create(
            user_profile=user_profile, area=area
        )
        if created:
            user_area.save()
            return Response(
                {"message": "Area added to user profile."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Area already exists in your profile."},
            status=status.HTTP_400_BAD_REQUEST,
        )
