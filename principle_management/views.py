from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from principle_management.filters import TrigramSimilaritySearchFilter
from principle_management.models import RoleModel, Principle
from principle_management.serializers import RoleModelSerializer, PrincipleSerializer


class RoleModelViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = RoleModel.objects.prefetch_related("principle").all()
    serializer_class = RoleModelSerializer
    filter_backends = [DjangoFilterBackend, TrigramSimilaritySearchFilter]
    search_fields = ['character_name']


class PrincipleViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = PrincipleSerializer
    filter_backends = [DjangoFilterBackend, TrigramSimilaritySearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        rolemodel_pk = self.kwargs.get('rolemodel_pk')
        if rolemodel_pk is not None:
            return Principle.objects.filter(characters__pk=rolemodel_pk)
        else:
            return Principle.objects.all()
