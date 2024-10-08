from datetime import datetime

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from journey.models import UserJourneyStatus, JourneyStep, Journey


class JourneyBaseService:
    def __init__(self, user_profile, journey=None):
        self.user_profile = user_profile
        self.journey = journey


class JourneyService(JourneyBaseService):

    @transaction.atomic
    def start_journey(self):
        if not self.journey:
            raise ValidationError("Journey not specified.")

        previous_journeys = Journey.objects.filter(
            journey_number__lt=self.journey.journey_number
        )

        completed_journey_ids = UserJourneyStatus.objects.filter(
            user_profile=self.user_profile,
            is_completed=True,
            journey__in=previous_journeys,
        ).values_list("journey_id", flat=True)

        uncompleted_previous_journeys = previous_journeys.exclude(
            id__in=completed_journey_ids
        )

        if uncompleted_previous_journeys.exists():
            uncompleted_journey_numbers = uncompleted_previous_journeys.values_list(
                "journey_number", flat=True
            )
            raise ValidationError(
                f"You cannot start Journey {self.journey.journey_number} because you have uncompleted "
                f"journey(s): {', '.join(map(str, uncompleted_journey_numbers))}."
            )

        first_step = self.journey.steps.first()
        journey_status, created = UserJourneyStatus.objects.get_or_create(
            user_profile=self.user_profile,
            journey=self.journey,
            defaults={"current_step": first_step, "is_completed": False},
        )

        if not created and not journey_status.is_completed:
            pass
        else:
            first_step = self.journey.steps.first()
            journey_status.is_completed = False
            journey_status.current_step = first_step
            journey_status.completed_steps = 0
            journey_status.started_at = datetime.now()
            journey_status.completed_at = None
            journey_status.save()
            return journey_status

        return journey_status

    def get_journey_status(self):
        try:
            user_journey_status = get_object_or_404(
                UserJourneyStatus.objects.select_related("journey"),
                user_profile=self.user_profile,
                journey=self.journey,
            )
            return user_journey_status
        except Http404:
            raise Http404({"not found": "You have not started this journey"})


class JourneyStepService(JourneyBaseService):

    def complete_journey_step(self):

        try:
            progress = UserJourneyStatus.objects.get(
                user_profile=self.user_profile, journey=self.journey
            )
        except UserJourneyStatus.DoesNotExist:
            raise ValidationError({"error": "You need to start journey first"})

        current_step = progress.current_step

        if current_step:
            next_step = JourneyStep.objects.filter(
                journey=self.journey, step_number=current_step.step_number + 1
            ).first()
        else:
            next_step = JourneyStep.objects.filter(journey=self.journey).first()

        if next_step:
            progress.current_step = next_step
            progress.completed_steps += 1
            progress.save()
            return current_step, False
        else:
            count_of_steps_in_journey = JourneyStep.objects.filter(
                journey=self.journey
            ).count()
            progress.is_completed = True
            progress.completed_steps = count_of_steps_in_journey
            progress.completed_at = datetime.now()
            progress.save()
            return current_step, True
