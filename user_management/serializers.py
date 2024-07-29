import datetime

from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from .models import User, UserProfile, OnboardingStep, UserOnboardingStatus, UserSatisfaction, PredefinedRole, UserRole, \
    PredefinedGoal, UserGoal


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User


class UserSerializer(BaseUserSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username']


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
    role = serializers.SerializerMethodField()

    class Meta:
        model = UserRole
        fields = ['id', 'role']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Remove fields that are None
        return {key: value for key, value in representation.items() if value is not None}

    def get_role(self, obj):
        if obj.role:
            return obj.role.title
        return obj.custom_role


class CreateUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'role', 'custom_role', 'is_custom']

    def validate_custom_role(self, value):
        return value.capitalize()

    def validate(self, data):
        role = data.get('role')
        custom_role = data.get('custom_role')

        if not role and not custom_role:
            raise serializers.ValidationError("Either 'role' or 'custom_role' must be provided.")
        if role and custom_role:
            raise serializers.ValidationError("'Predefined role' and 'custom_role' cannot both be provided "
                                              "simultaneously.")
        if UserRole.objects.filter(custom_role__iexact=custom_role).exists():
            raise serializers.ValidationError({'duplicated': "A role with that title already exists, "
                                                             "select from list"})

        return data

    def create(self, validated_data):

        with transaction.atomic():
            user_profile_id = self.context['user_profile_id']
            role = self.validated_data['role']
            custom_title = self.validated_data['custom_role']
            if role:
                user_role = UserRole.objects.create(role=role)
            else:
                predefined_role = PredefinedRole.objects.create(title=custom_title)
                user_role = UserRole.objects.create(custom_role=custom_title, role_id=predefined_role.id,
                                                    is_custom=True)
            user_profile = UserProfile.objects.get(id=user_profile_id)
            user_profile.roles.add(user_role)
            user_profile.save()

            return user_role

    def get_roles(self, obj):
        if obj.role:
            return obj.role.title
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    roles = UserRoleSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'location', 'profile_picture', 'ai_assistant_model', 'birth_date',
                  'current_habits', 'dashboard_customization', 'notification_preferences', 'bio', 'roles', 'goals',
                  ]


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'location', 'profile_picture', 'ai_assistant_model', 'birth_date',
                  'current_habits', 'dashboard_customization', 'notification_preferences', 'bio', 'roles', 'goals',
                  ]

    def update(self, instance, validated_data):
        initial_data = UserProfileSerializer(instance).data
        instance = super().update(instance, validated_data)
        updated_data = UserProfileSerializer(instance).data
        # profile_picture = validated_data.pop('profile_picture', None)
        # if profile_picture is not None:
        #     instance.profile_picture = profile_picture

        '''returning only changed data
        '''
        changed_data = {field: updated_data[field] for field in updated_data if
                        initial_data[field] != updated_data[field]}
        return changed_data

    def validate_birth_date(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value


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
        fields = ['id', 'goal_title', 'custom_title', 'custom_description', 'is_initial', 'is_custom']
