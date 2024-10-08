from django.db import transaction
from django.db.models import Sum, F

from life_sphere.models import LifeSphere
from onboarding.models import OnboardingQuestion, OnboardingProgress, UserResponse, AnswerOption
from user_management.models import UserBalance


class OnboardingService:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.last_response = self.user_profile.responses.select_related('user_answer').first()
        self.answered_question_ids = self.user_profile.responses.values_list('question_id', flat=True)

    def _get_tailored_question(self):
        if self.last_response:
            user_answer_id = self.last_response.user_answer_id
            answer_option = AnswerOption.objects.get(id=user_answer_id)
            tailored_question = answer_option.tailored_question
            if answer_option.tailored_question:
                return tailored_question
            return None

    def _get_next_unanswered_question(self):
        next_question = (OnboardingQuestion.objects.filter(
            order__gt=0
        ).
                         exclude(
            id__in=self.answered_question_ids,
        ).first())
        return next_question

    def get_next_question(self):
        if self.last_response:
            next_question = self._get_tailored_question()
            if next_question:
                return next_question
        return self._get_next_unanswered_question()

    def update_onboarding_progress(self):
        onboarding_progress, created = OnboardingProgress.objects.get_or_create(
            user_profile=self.user_profile,
            defaults={'completed_questions': 0}
        )
        onboarding_progress.completed_questions += 1
        onboarding_progress.save()

    def save_initial_user_balance(self):
        """
        Calculates the total points per life sphere and saves the initial user balance.
        """
        # Aggregate total points per life sphere for the user's responses
        life_sphere_points = (
            UserResponse.objects
            .filter(user_profile=self.user_profile)
            .values(
                life_sphere_id=F('question__life_sphere__id'),
                life_sphere_title=F('question__life_sphere__title')
            )
            .annotate(total_points=Sum('user_answer__points'))
        )

        if not life_sphere_points:
            return

        life_sphere_scores = {
            item['life_sphere_id']: item['total_points'] or 0
            for item in life_sphere_points
        }

        life_spheres = LifeSphere.objects.filter(id__in=life_sphere_scores.keys())
        life_sphere_map = {ls.id: ls for ls in life_spheres}

        user_balances = [
            UserBalance(
                user_profile=self.user_profile,
                life_sphere=life_sphere_map[ls_id],
                score=score
            )
            for ls_id, score in life_sphere_scores.items()
            if ls_id in life_sphere_map
        ]

        with transaction.atomic():
            UserBalance.objects.filter(
                user_profile=self.user_profile,
                life_sphere__in=life_spheres
            ).delete()
            UserBalance.objects.bulk_create(user_balances)

    def complete_onboarding(self):
        """
        Handles actions to perform when the user completes the onboarding questionnaire.
        """
        self.save_initial_user_balance()
