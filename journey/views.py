from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from journey.models import (
    Journey,
    JourneyStep,
)
from journey.serializers import (
    JourneySerializer,
    JourneyStepSerializer,
    UserJourneyStatusSerializer,
    NextStepSerializer, StartJourneySerializer, )
from journey.services.journey_service import JourneyService, JourneyStepService


class JourneyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Journey.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StartJourneySerializer
        return JourneySerializer

    @action(detail=True, url_path="start", methods=["post"])
    def start_journey(self, request, pk=None):
        user_profile = request.user.user_profile
        journey = self.get_object()
        services = JourneyService(user_profile, journey)
        services.start_journey()
        return Response(f'{journey} has been started', status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], url_path="status")
    def journey_status(self, request, pk=None):
        user_profile = self.request.user.user_profile
        journey = get_object_or_404(Journey, pk=pk)
        services = JourneyService(user_profile, journey)
        journey_status = services.get_journey_status()
        serializer = UserJourneyStatusSerializer(journey_status)
        return Response(serializer.data, status.HTTP_200_OK)


class JourneyStepViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):

    def get_queryset(self):
        journey_pk = self.kwargs.get("journey_pk")
        return JourneyStep.objects.filter(journey=journey_pk).select_related("journey")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NextStepSerializer
        return JourneyStepSerializer

    @action(detail=False, methods=["post"], url_path="complete")
    def complete_step(self, request, *args, **kwargs):
        journey = self.kwargs.get("journey_pk")
        user_profile = self.request.user.user_profile
        service = JourneyStepService(user_profile, journey)
        next_step, is_completed = service.complete_journey_step()
        NextStepSerializer(next_step)
        if is_completed:
            return Response(
                {"info": f"You have successfully completed last step: : '{next_step}' in journey {journey}"}
            )

        return Response({"info": f"Step '{next_step.step_number}', '{next_step}' completed"},
                        status=status.HTTP_200_OK)
