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
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):

    queryset = JourneyStep.objects.select_related('journey').all()


    def get_serializer_class(self):
        if self.request.method == "PUT":
            return StartJourneyStepSerializer
        return JourneyStepSerializer

    def update(self, request, *args, **kwargs):
        """
        Handle the logic for starting or updating a user's journey step.
        """

        user_profile = self.request.user.user_profile
        step = self.get_object()
        journey = step.journey

        with transaction.atomic():
            # Get the user's journey status
            user_journey_status, journey_created = (
                UserJourneyStatus.objects.get_or_create(
                    user_profile=user_profile,
                    journey=journey,
                    defaults={"current_step": step, "started_at": timezone.now()},
                )
            )
            if journey_created:
                user_journey_status.current_step = step
                user_journey_status.save()

            user_journey_step_status, step_created = (
                UserJourneyStepStatus.objects.get_or_create(
                    user_profile=user_profile,
                    step=step,
                )
            )

            if step_created:
                user_journey_step_status.save()
                return Response(
                    {"message": "Journey step and journey started successfully."},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"message": "Journey step already started."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserJourneyStatusViewSet(ListModelMixin, GenericViewSet):
    queryset = UserJourneyStatus.objects.all()
    serializer_class = UserJourneyStatusSerializer
    permission_classes = [IsAuthenticated]
