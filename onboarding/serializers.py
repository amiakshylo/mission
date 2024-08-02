from rest_framework import serializers

from onboarding.models import OnboardingStep, UserOnboardingStatus
from user_management.models import UserProfile


class OnboardingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingStep
        fields = ['step_number', 'title', 'description']


class UserOnboardingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOnboardingStatus
        fields = ['user_profile', 'current_step', 'is_completed']


class OnboardingStep1Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'location']


class OnboardingStep2Serializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = UserProfile
        fields = ['birth_date']


class OnboardingStep3Serializer(serializers.Serializer):
    roles = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )
    custom_roles = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        allow_empty=True
    )


class OnboardingStep4Serializer(serializers.Serializer):
    goals = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )
    custom_goals = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        ),
        allow_empty=True
    )
