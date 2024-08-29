from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from life_sphere.models import LifeSphere
from onboarding.models import OnboardingResponse, OnboardingQuestion, UserProgress
from onboarding.serializers import OnboardingQuestionSerializer, OnboardingResponseSerializer


class OnboardingViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = OnboardingQuestion.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OnboardingResponseSerializer
        return OnboardingQuestionSerializer




    def get_serializer_context(self):
        user_profile = self.request.user.user_profile.id
        progress, created = UserProgress.objects.get_or_create(user_profile=user_profile,
                                                               defaults={'current_life_sphere': LifeSphere.objects.first()}
                                                               )
        life_sphere = progress.current_life_sphere

        # Get all questions for the current life sphere
        all_questions = OnboardingQuestion.objects.filter(life_sphere=life_sphere)

        # Exclude completed or skipped questions
        available_questions = all_questions.exclude(id__in=progress.completed_questions.all()).exclude(
            id__in=progress.skipped_questions.all())

        # Determine the next question or if onboarding is done
        if available_questions.exists():
            next_question = available_questions.first()  # This can be more sophisticated if needed
            is_last_question = available_questions.count() == 1 and progress.completed_questions.filter(
                life_sphere=life_sphere).count() >= 2
        else:
            next_question = None
            is_last_question = True

        context = {
            'user_profile': user_profile,
            'question_id': next_question.id if next_question else None,
            'is_last_question': is_last_question,
            'current_life_sphere': life_sphere,
        }

        return context

    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        question_id = self.request.query_params.get('id')
        progress = UserProgress.objects.get(user_profile=user_profile)

        # Save the response
        serializer.save(user_profile=user_profile)

        # Update progress
        if question_id:
            question = OnboardingQuestion.objects.get(id=question_id)
            progress.completed_questions.add(question)

            # Move to the next life sphere if this was the last question
            if self.get_serializer_context()['is_last_question']:
                # Logic to move to the next life sphere or complete onboarding
                next_life_sphere = LifeSphere.objects.filter(id__gt=progress.current_life_sphere.id).first()
                if next_life_sphere:
                    progress.current_life_sphere = next_life_sphere
                else:
                    progress.current_life_sphere = None  # Onboarding complete

            progress.save()







