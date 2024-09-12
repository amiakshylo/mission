from rest_framework import serializers

from onboarding.models import OnboardingQuestion, AnswerOption, OnboardingAnswer


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id',
                  'option',
                  ]


class OnboardingQuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = OnboardingQuestion
        fields = ['id',
                  'text',
                  'options',
                  ]


class OnboardingAnswerSerializer(serializers.ModelSerializer):


    class Meta:
        model = OnboardingAnswer
        fields = ['user_answer'
                  ]
