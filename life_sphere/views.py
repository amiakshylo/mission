
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import LifeSphere
from .serializers import LifeSphereSerializer


class LifeSphereViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):

    serializer_class = LifeSphereSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LifeSphere.objects.all()






