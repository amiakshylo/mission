import datetime

from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from goal_task_management.models import Goal
from habit_management.serializers import UserHabitSerializer
from .models import User, UserProfile, UserRole, UserGoal


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User


class UserSerializer(BaseUserSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username']


class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ['id', 'goal', 'custom_goal', 'progress', 'is_completed', 'is_active']




class CreateUserGoalSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all(), required=False, allow_null=True)

    class Meta:
        model = UserGoal
        fields = ['id', 'goal', 'custom_goal', 'is_custom']


    def validate_custom_goal(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Custom goal must be a string.")
        return value.capitalize()

    def validate(self, data):
        goal = data.get('goal')
        custom_goal = data.get('custom_goal')

        if not goal and not custom_goal:
            raise serializers.ValidationError("Either 'goal' or 'custom_goal' must be provided.")
        if goal and custom_goal:
            raise serializers.ValidationError("'goal' and 'custom_goal' cannot both be provided simultaneously.")
        if UserGoal.objects.filter(goal__exact=goal).exists():
            raise serializers.ValidationError(
                {'duplicated': "A goal with that title already exists, select from list."})

        return data

    def create(self, validated_data):
        with transaction.atomic():
            user_profile_id = self.context['user_profile_id']
            user_profile = UserProfile.objects.get(user=user_profile_id)
            goal_id = validated_data.pop('goal', None)
            custom_goal = validated_data.pop('custom_goal', None)

            if goal_id:
                goal = UserGoal.objects.get(id=goal_id)
                user_goal = UserGoal.objects.create(
                    user_profile=user_profile,
                    goal=goal,
                    is_initial=validated_data.get('is_initial', False),

                )
            else:
                user_goal = UserGoal.objects.create(
                    user_profile=user_profile,
                    custom_goal=custom_goal,
                    is_custom=True,

                )
            user_profile.goals.add(user_goal)
            user_profile.save()

            return user_goal




class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'role', 'group_name', 'custom_role']




class CreateUserRoleSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all(), required=False, allow_null=True)

    class Meta:
        model = UserRole
        fields = ['role', 'custom_role']

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
        if custom_role and UserRole.objects.filter(custom_role__iexact=custom_role).exists():
            raise serializers.ValidationError({'duplicated': "A role with that title already exists, select from list"})

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
                user_profile.user_roles.add(role)
                user_role = role
            else:
                user_role = UserRole.objects.create(
                    custom_role=custom_role,
                    group_name=group_name,
                    is_custom=True,
                )
                user_profile.user_roles.add(user_role)
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
