from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from life_sphere.models import LifeSphere
from onboarding.models import OnboardingQuestion, OnboardingAnswer, AnswerOption
from onboarding.serializers import OnboardingQuestionSerializer, OnboardingAnswerSerializer


class OnboardingViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = OnboardingQuestion.objects.prefetch_related('options')

    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):

        if self.request.method == 'PUT':
            return OnboardingAnswerSerializer
        return OnboardingQuestionSerializer

    def update(self, request, *args, **kwargs):
        user_profile = request.user.user_profile
        question = self.get_object()

        answer = request.data.get('user_answer')
        try:
            answer_option = question.options.get(id=answer)
        except AnswerOption.DoesNotExist:
            return Response({'error': 'Invalid answer option'}, status=status.HTTP_400_BAD_REQUEST)

        # If an answer already exists, update it
        if OnboardingAnswer.objects.filter(user_profile=user_profile, question=question).exists():
            OnboardingAnswer.objects.filter(user_profile=user_profile, question=question).update(
                user_answer=answer_option)
            return Response({'message': 'Answer updated successfully'}, status=status.HTTP_200_OK)

        # Create a new answer if it doesn't exist
        OnboardingAnswer.objects.update_or_create(user_profile=user_profile, question=question,
                                                  user_answer=answer_option)
        return Response({'message': 'Answer created successfully'}, status=status.HTTP_201_CREATED)




