from django.db import transaction
from rest_framework import status
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
    UserJourneyStatusSerializer,
)


class JourneyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    permission_classes = [IsAuthenticated]


class JourneyStepViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        journey_pk = self.kwargs.get("journey_pk")
        return JourneyStep.objects.filter(journey_id=journey_pk).select_related(
            "journey"
        )

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
