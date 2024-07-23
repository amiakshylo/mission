from datetime import datetime, date

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User, UserProfile, OnboardingStep, UserOnboardingStatus, UserSatisfaction, PredefinedRole, UserRole, \
    PredefinedGoal, UserGoal


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('email', 'password')


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'gender', 'location', 'profile_picture', 'ai_assistant_model', 'birth_date',
                  'current_habits', 'dashboard_customization', 'notification_preferences', 'roles', 'goals']


class EditUserProfileSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'location', 'profile_picture', 'ai_assistant_model', 'birth_date',
                  'dashboard_customization', 'notification_preferences']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserCreateSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
        return super(EditUserProfileSerializer, self).update(instance, validated_data)


class OnboardingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingStep
        fields = ['step_number', 'title', 'description']


class UserOnboardingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOnboardingStatus
        fields = ['user', 'current_step', 'is_completed']


class UserSatisfactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSatisfaction
        fields = ['user_profile', 'category', 'score']


class OnboardingStep1Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'location']


class OnboardingStep2Serializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = UserProfile
        fields = ['birth_date']




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


class PredefinedRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedRole
        fields = ['id', 'title', 'description', 'group']


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'predefined_role', 'custom_title', 'custom_group', 'is_custom']


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


class PredefinedGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedGoal
        fields = ['id', 'title', 'description', 'type']


class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ['id', 'predefined_goal', 'custom_title', 'custom_description', 'is_initial', 'is_custom']
