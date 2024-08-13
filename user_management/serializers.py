import datetime

from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from category_management.models import SubCategory
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


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'role', 'group_name', 'custom_role']


class UserGoalSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all())

    class Meta:
        model = UserGoal
        fields = ['id', 'goal', 'custom_goal', 'is_custom']


class GoalSuggestionInputSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    user_input = serializers.CharField(required=False)


class GoalAutocompleteSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    custom_goal = serializers.CharField(required=False, allow_blank=True)


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description']


class CreateUserGoalSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(queryset=Goal.objects.all(), required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), required=True)

    class Meta:
        model = UserGoal
        fields = ['id', 'goal', 'category', 'custom_goal', 'is_custom']

    def validate(self, data):
        if data.get('is_custom') and not data.get('custom_goal'):
            raise serializers.ValidationError("Custom goal must be provided if 'is_custom' is True.")
        if not data.get('is_custom') and not data.get('goal'):
            raise serializers.ValidationError("A goal must be selected.")
        return data


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
