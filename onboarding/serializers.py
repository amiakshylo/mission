from rest_framework import serializers

from onboarding.models import OnboardingQuestion, OnboardingResponse


class OnboardingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingQuestion
        fields = ['id', 'text', 'life_sphere']


class OnboardingResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingResponse
        fields = ['response']

    def create(self, validated_data):
        user_profile = self.context.get('user_profile')
        question_id = self.context.get('question_id')

        onboarding_response = OnboardingResponse.objects.filter(user_profile=user_profile,
                                                                question_id=question_id).first()

        if onboarding_response:
            # Update the existing response
            onboarding_response.response = validated_data.get('response')
            onboarding_response.save()
            return onboarding_response

        return OnboardingResponse.objects.create(user_profile=user_profile, question_id=question_id, **validated_data)

