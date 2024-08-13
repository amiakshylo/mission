import datetime

from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from goal_task_management.models import Goal
from goal_task_management.serializers import GoalSerializer
from habit_management.serializers import UserHabitSerializer
from .models import User, UserProfile, Role, UserGoal


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User


class UserSerializer(BaseUserSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username']


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'role', 'group_name']


class UserGoalSerializer(serializers.ModelSerializer):
    goal = GoalSerializer()

    class Meta:
        model = UserGoal
        fields = ['id', 'goal', 'paused', 'is_active', 'progress', 'goal_type', 'is_completed', 'due_date']









class EditUserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ['paused', 'progress', 'is_completed']



class CreateUserGoalSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all(), required=False, allow_null=True)

    class Meta:
        model = UserGoal
        fields = ['id', 'goal', 'custom_goal', 'goal_type', 'due_date']

    def validate(self, data):
        if not data.get('goal') and not data.get('custom_goal'):
            raise serializers.ValidationError("Either 'goal' or 'custom_goal' must be provided.")
        if data.get('custom_goal') and not data.get('category'):
            raise serializers.ValidationError("Select a category for your custom goal")
        if UserGoal.objects.filter(user_profile=self.context.get('user_profile'), goal=data.get('goal')).exists():
            raise serializers.ValidationError("This goal is already set up by you, please choose another goal or create"
                                              " a new one.")
        return data








class CreateUserRoleSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Role
        fields = ['role', 'custom_role', 'group_name']

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
        if custom_role and Role.objects.filter(custom_role__iexact=custom_role).exists():
            raise serializers.ValidationError({'duplicated': "A role with that title already exists, select from list"})

        if custom_role and not data.get('group_name'):
            raise serializers.ValidationError("Please define a group name for the custom role")

        return data

    def create(self, validated_data):
        with transaction.atomic():
            user_profile_id = self.context.get('user_profile_id')

            try:
                user_profile = UserProfile.objects.get(pk=user_profile_id)
            except UserProfile.DoesNotExist:
                raise serializers.ValidationError("UserProfile does not exist.")

            role = validated_data.get('role')
            custom_role = validated_data.get('custom_role')
            group_name = validated_data.get('group_name')

            if role:
                user_profile.roles.add(role)
                user_role = role
            else:
                user_role = Role.objects.create(
                    role=custom_role,
                    group_name=group_name,
                    is_custom=True,
                )
                user_profile.roles.add(user_role)
            user_profile.save()

            return user_role


class UserProfileSerializer(serializers.ModelSerializer):
    user_roles = UserRoleSerializer(many=True, read_only=True)
    user_habits = UserHabitSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'location', 'profile_picture', 'birth_date',
                  'bio', 'user_roles',
                  'user_habits'
                  ]


class EditUserProfileSerializer(serializers.ModelSerializer):
    user_roles = UserRoleSerializer(many=True)
    user_habits = UserHabitSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ['gender', 'location', 'profile_picture', 'birth_date',
                  'bio',

                  ]

    def update(self, instance, validated_data):
        initial_data = UserProfileSerializer(instance).data
        instance = super().update(instance, validated_data)
        updated_data = UserProfileSerializer(instance).data

        '''returning only changed data
        '''
        changed_data = {field: updated_data[field] for field in updated_data if
                        initial_data[field] != updated_data[field]}
        return changed_data

    def validate_birth_date(self, value):
        if value > datetime.date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value
