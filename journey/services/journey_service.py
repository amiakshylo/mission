from core.services.base_services import UserProfileService
from journey.models import UserJourneyStatus


class StartJourney(UserProfileService):

    def update_journey_status(self, journey):
        journey_status, created = UserJourneyStatus.objects.get_or_create(
            user_profile=self.user_profile,
            journey=journey,

        )
        if created:



