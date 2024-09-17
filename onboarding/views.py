from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from . import utils
from user_management.utils import save_initial_user_balance

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from onboarding.models import OnboardingQuestion, UserResponse
from onboarding.serializers import UserResponseSerializer, QuestionSerializer


class OnboardingViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserResponse.objects.select_related("question")
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="next-question")
    def next_question(self, request):
        user_profile = request.user.user_profile
        answered_question_ids = user_profile.responses.values_list(
            "question_id", flat=True
        )

        # Get the last response
        last_response = user_profile.responses.order_by("-timestamp").first()

        if last_response:
            # Attempt to find a follow-up question triggered by the last answer
            follow_up_question = OnboardingQuestion.objects.filter(
                is_followup=True, triggering_options=last_response.user_answer
            ).exclude(id__in=answered_question_ids)

            if follow_up_question.exists():
                # Found a follow-up question
                next_question = follow_up_question.first()
            else:
                # No follow-up; get the next unanswered non-follow-up question in the same life sphere
                next_question = (
                    OnboardingQuestion.objects.filter(is_followup=False)
                    .exclude(id__in=answered_question_ids)
                    .order_by("order")
                    .first()
                )
        else:
            # No previous responses; get the first non-follow-up question
            next_question = (
                OnboardingQuestion.objects.filter(is_followup=False)
                .exclude(id__in=answered_question_ids)
                .order_by("order")
                .first()
            )

        if not next_question:
            initial_user_balance = utils.calculate_total_points_per_life_sphere(
                user_profile
            )
            save_initial_user_balance(user_profile)
            return Response(
                f"Current life sphere balance: {initial_user_balance}",
                status=status.HTTP_200_OK,
            )

        serializer = QuestionSerializer(next_question)
        return Response(serializer.data)

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        return {"user_profile": user_profile}
