from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.utils import timezone
from journey.models import (
    Journey,
    JourneyStep,
    UserJourneyStatus,
    UserJourneyStepStatus,
)
from journey.serializers import (
    JourneySerializer,
    JourneyStepSerializer,
    StartJourneyStepSerializer,
    UserJourneyStatusSerializer, UserJourneyStartSerializer,
)
from journey.services.journey_service import JourneyService


class JourneyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Journey.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserJourneyStatusSerializer
        return JourneySerializer


    @action(detail=True, url_path='start', methods=['post'])
    def start_journey(self, request, pk=None):
        user_profile = request.user.user_profile
        journey = self.get_object()

        services = JourneyService(user_profile, journey)
        journey_status = services.start_journey()

        serializer = UserJourneyStatusSerializer(journey_status)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='status')
    def journey_status(self, request, pk=None):
        user_profile = self.request.user.user_profile
        services = JourneyService(user_profile, None)
        try:
            journey_status = services.get_current_journey_status()
        except Http404:
            return Response(
                {'No found': 'You have not started any journey yet.'},
                status=status.HTTP_200_OK
            )
        serializer = UserJourneyStatusSerializer(journey_status)
        return Response(serializer.data, status.HTTP_200_OK)



class JourneyStepViewSet(
    ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    serializer_class = JourneyStepSerializer

    def get_queryset(self):
        journey_pk = self.kwargs.get('journey_pk')
        return JourneyStep.objects.filter(journey=journey_pk).select_related('journey')



