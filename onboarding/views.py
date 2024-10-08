from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from onboarding.models import UserResponse, OnboardingProgress
from onboarding.serializers import (
    UserResponseSerializer,
    QuestionSerializer,
    OnboardingProgressSerializer,
)
from .services.onboardind_service import OnboardingService


class OnboardingViewSet(CreateModelMixin, GenericViewSet):
    queryset = UserResponse.objects.select_related("question")
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            user_profile = request.user.user_profile
            service = OnboardingService(user_profile)
            service.update_onboarding_progress()
        return response

    @action(detail=False, methods=["get"], url_path="next-question")
    def next_question(self, request):
        user_profile = request.user.user_profile
        service = OnboardingService(user_profile)
        next_question = service.get_next_question()

        if not next_question:
            service.complete_onboarding()
            return Response(
                {
                    "message": f"All questions have been answered"
                },
                status=status.HTTP_200_OK,
            )

        serializer = QuestionSerializer(next_question)

        return Response(serializer.data)

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        return {"user_profile": user_profile}

    @action(detail=False, methods=["get"], url_path="progress")
    def onboarding_progress(self, request):
        user_profile = self.request.user.user_profile
        onboarding_progress = get_object_or_404(
            OnboardingProgress, user_profile=user_profile
        )
        serializer = OnboardingProgressSerializer(onboarding_progress)
        return Response(serializer.data)
