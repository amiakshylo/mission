
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

        if self.journey.pk - self._finished_journey() > 1:
            raise ValidationError(
                f'Cannot start journey {self.journey.journey_number} until previous is uncompleted ')

        first_step = self.journey.steps.order_by('step_number').first()
        journey_status, created = UserJourneyStatus.objects.get_or_create(
            user_profile=self.user_profile,
            journey=self.journey,
            current_step=first_step
        )

        if not created:
            raise ValidationError(f'Journey {self.journey.journey_number} is already started.')

        if self._has_incomplete_journey():
            raise ValidationError(
                'Cannot start new journey until previous is uncompleted.'
            )

        return journey_status


    def get_current_journey_status(self):
        journey_status = get_object_or_404(
            UserJourneyStatus.objects.select_related('journey'),
            user_profile=self.user_profile
        )
        return journey_status


    def _has_incomplete_journey(self):
        return UserJourneyStatus.objects.filter(user_profile=self.user_profile,
                                                is_completed=False
                                                ).exists()

    def _finished_journeys(self):
        return UserJourneyStatus.objects.filter(
            user_profile=self.user_profile
        ).count()

    def _finished_journey(self):
        return UserJourneyStatus.objects.filter(user_profile=self.user_profile, is_completed=True).count()






