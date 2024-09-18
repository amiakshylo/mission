from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from onboarding.models import UserResponse
from onboarding.serializers import UserResponseSerializer, QuestionSerializer
from .services.onboardind_service import OnboardingService


class OnboardingViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserResponse.objects.select_related("question")
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="next-question")
    def next_question(self, request):
        user_profile = request.user.user_profile
        service = OnboardingService(user_profile)
        next_question = service.next_question()

        if not next_question:
            service.complete_onboarding()
            return Response(
                {"message": f"All questions are answered. Current life sphere balance: {service.initial_user_balance}"},
                status=status.HTTP_200_OK,
            )

        serializer = QuestionSerializer(next_question)
        return Response(serializer.data)


    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        return {"user_profile": user_profile}
