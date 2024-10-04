from datetime import datetime

from django.db import transaction
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
                f"You cannot start Journey {self.journey.journey_number} because you have uncompleted previous "
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
        elif not created and journey_status.is_completed:
            raise ValidationError(
                f"Journey {self.journey.journey_number} has already been completed."
            )

        return journey_status

    def get_current_journey_status(self):
        user_journey_status = get_object_or_404(
            UserJourneyStatus, user_profile=self.user_profile, is_completed=False
        )
        if user_journey_status:
            return user_journey_status
        raise ValidationError("You have not started any journey")


class JourneyStepService(JourneyBaseService):

    def initialize_next_journey_step(self):
        try:
            progress = UserJourneyStatus.objects.get(
                user_profile=self.user_profile, journey=self.journey
            )
        except UserJourneyStatus.DoesNotExist:
            return ValidationError("You need to complete previous journey")

        current_step = progress.current_step

        if current_step:
            next_step = JourneyStep.objects.filter(
                journey=self.journey, step_number=current_step.step_number + 1
            ).first()
        else:
            next_step = (
                JourneyStep.objects.filter(journey=self.journey)
                .order_by("step_number")
                .first()
            )

        if next_step:
            progress.current_step = next_step
            progress.completed_steps += 1
            progress.save()
            return progress, False
        else:
            progress.is_completed = True
            progress.completed_steps += 1
            progress.completed_at = datetime.now()
            progress.save()
            return progress, True
