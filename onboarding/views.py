from django.shortcuts import render
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from onboarding.models import OnboardingResponse, OnboardingQuestion
from onboarding.serializers import OnboardingQuestionSerializer, OnboardingResponseSerializer


class OnboardingViewSet(ModelViewSet):
    queryset = OnboardingQuestion.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OnboardingResponseSerializer
        return OnboardingQuestionSerializer

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        question_id = self.request.query_params.get('id')

        return {'user_profile': user_profile, 'question_id': question_id}







