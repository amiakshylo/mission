from django.db import transaction
from django.db.models import F, Sum
from django.utils.functional import cached_property

from life_sphere.models import LifeSphere

from onboarding.models import OnboardingQuestion, UserResponse
from user_management.models import UserBalance


class OnboardingService:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.answered_question_ids = self.user_profile.responses.values_list('question_id', flat=True)
        self.last_response = self.user_profile.responses.select_related('user_answer').order_by("-timestamp").first()

    def _get_follow_up_question(self):
        """
        Attempts to find a follow-up question triggered by the user's last answer.
        """
        if self.last_response:
            follow_up_question = OnboardingQuestion.objects.filter(
                is_followup=True,
                triggering_options=self.last_response.user_answer
            ).exclude(
                id__in=self.answered_question_ids
            ).first()
            return follow_up_question
        return None

    def _get_next_unanswered_question(self):
        """
        Retrieves the next unanswered non-follow-up question.
        """
        next_question = OnboardingQuestion.objects.filter(
            is_followup=False
        ).exclude(
            id__in=self.answered_question_ids
        ).order_by('order').first()
        return next_question

    def next_question(self):
        """
        Determines the next question to present to the user.
        """
        if self.last_response:
            next_question = self._get_follow_up_question()
            if next_question:
                return next_question

        return self._get_next_unanswered_question()

    @cached_property
    def initial_user_balance(self):
        """
        Calculates and caches the total points per life sphere.
        """
        return self.calculate_total_points_per_life_sphere()

    def calculate_total_points_per_life_sphere(self):
        """
        Aggregates total points per life sphere for the user's responses.
        """
        life_sphere_points = (
            UserResponse.objects.filter(user_profile=self.user_profile)
            .values(life_sphere_id=F('question__life_sphere__id'), life_sphere_title=F('question__life_sphere__title'))
            .annotate(total_points=Sum('user_answer__points'))
        )

        life_sphere_points_dict = {
            item['life_sphere_title']: item['total_points'] or 0
            for item in life_sphere_points
        }

        return life_sphere_points_dict

    def save_initial_user_balance(self):
        """
        Saves the initial user balance using the calculated life sphere points.
        """
        initial_user_balance = self.initial_user_balance
        life_sphere_titles = initial_user_balance.keys()


        life_spheres = LifeSphere.objects.filter(title__in=life_sphere_titles)
        life_sphere_map = {ls.title: ls for ls in life_spheres}


        user_balances_to_create = []
        user_balances_to_update = []

        existing_balances = UserBalance.objects.filter(
            user_profile=self.user_profile,
            life_sphere__in=life_spheres
        )
        existing_balance_map = {ub.life_sphere_id: ub for ub in existing_balances}


        for life_sphere_title, score in initial_user_balance.items():
            life_sphere = life_sphere_map.get(life_sphere_title)
            if life_sphere:
                existing_balance = existing_balance_map.get(life_sphere.id)
                if existing_balance:
                    existing_balance.score = score
                    user_balances_to_update.append(existing_balance)
                else:
                    user_balances_to_create.append(UserBalance(
                        user_profile=self.user_profile,
                        life_sphere=life_sphere,
                        score=score
                    ))

        with transaction.atomic():
            if user_balances_to_create:
                UserBalance.objects.bulk_create(user_balances_to_create)
            if user_balances_to_update:
                UserBalance.objects.bulk_update(user_balances_to_update, ['score'])

    def complete_onboarding(self):
        """
        Handles actions to perform when the user completes the onboarding questionnaire.
        """
        self.save_initial_user_balance()





