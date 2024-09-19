from rest_framework import serializers, status
from rest_framework.response import Response

from onboarding.models import OnboardingQuestion, AnswerOption, UserResponse, OnboardingProgress


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["id", "answer"]


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)
    text = serializers.CharField(read_only=True)

    class Meta:
        model = OnboardingQuestion
        fields = ["id", "text", "options"]


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = ["question", "user_answer"]

    def validate(self, attrs):
        selected_answer = attrs.get("user_answer")
        question = attrs.get("question")

        if not question:
            raise serializers.ValidationError("Question instance is required.")
        if not selected_answer:
            raise serializers.ValidationError("Selected answer is required.")

        if selected_answer.question_id != question.id:
            raise serializers.ValidationError(
                "Selected answer does not belong to this question."
            )

        user_profile = self.context["user_profile"]
        if UserResponse.objects.filter(
                user_profile=user_profile, question=question
        ).exists():
            raise serializers.ValidationError(
                "You have already responded to this question."
            )

        return attrs

    def create(self, validated_data):
        validated_data["user_profile"] = self.context["user_profile"]
        return UserResponse.objects.create(**validated_data)


class OnboardingProgressSerializer(serializers.ModelSerializer):
    questions_remain = serializers.SerializerMethodField()

    class Meta:
        model = OnboardingProgress
        fields = ['completed_questions', 'questions_remain']

    def get_questions_remain(self, obj: OnboardingProgress):
        return obj.calculate_remaining_questions()
