from rest_framework.viewsets import ModelViewSet

from journey.models import Journey
from journey.serializers import JourneySerializer
from user_management.permissions import IsAdminOrReadOnly


class JourneyViewSet(ModelViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    permission_classes = [IsAdminOrReadOnly]
