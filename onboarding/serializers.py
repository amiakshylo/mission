from rest_framework import serializers, status
from rest_framework.response import Response

from onboarding.models import OnboardingQuestion, AnswerOption, UserResponse


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id',
                  'option'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)
    text = serializers.CharField(read_only=True)

    class Meta:
        model = OnboardingQuestion
        fields = ['id',
                  'text',
                  'options'
                  ]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserResponse
        fields = ['user_answer']


    def validate(self, attrs):
        selected_answer = attrs.get('user_answer')
        question = int(self.context.get('question'))

        if not question:
            raise serializers.ValidationError("Question instance is required.")

        if selected_answer.question_id != question:
            print(type(selected_answer.question_id), type(question))
            raise serializers.ValidationError("Selected answer does not belong to this question.")

        user_profile = self.context['user_profile']
        if UserResponse.objects.filter(user_profile=user_profile, question=question).exists():
            raise serializers.ValidationError("You have already responded to this question.")

        return attrs

    def create(self, validated_data):
        user_profile = self.context['user_profile']
        question = self.context.get('question')
        user_response = UserResponse.objects.create(**validated_data, user_profile=user_profile, question_id=question)
        return user_response
