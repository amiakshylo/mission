import datetime

from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from category_management.serializers import CategorySerializer
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
    category = serializers.StringRelatedField()

    class Meta:
        model = Role
        fields = ['id', 'title', 'category']


class CreateUserRoleSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Role
        fields = ['role', 'custom_title']

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


        return data

    def create(self, validated_data):
        with transaction.atomic():
            user_profile = self.context.get('user_profile')
            print(user_profile)


            role = validated_data.get('role')
            custom_role = validated_data.get('custom_role')


            if role:
                user_profile.roles.add(role)
                user_role = role
            else:
                user_role = Role.objects.create(
                    role=custom_role,
                    is_custom=True,
                )
                user_profile.roles.add(user_role)
            user_profile.save()

            return user_role


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





class UserProfileSerializer(serializers.ModelSerializer):
    roles = UserRoleSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'gender', 'location', 'profile_picture', 'birth_date',
                  'roles'
                  ]


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'location', 'profile_picture', 'birth_date',
                  ]

    def validate_birth_date(self, value):
        if value is not None and value > datetime.date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value
