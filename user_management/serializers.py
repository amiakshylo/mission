import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.model_choices import UserProfileChoices
from goal_task.models import Goal
from goal_task.serializers import GoalSerializer
from principle.models import Principle
from .models import (
    User,
    UserProfile,
    Role,
    UserGoal,
    UserArea,
    UserBalance, UserPrinciple, )


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User


class UserSerializer(BaseUserSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ["id", "email", "username"]


class RoleSerializer(serializers.ModelSerializer):
    type = serializers.CharField()

    class Meta:
        model = Role
        fields = ["id", "title", "type"]


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "title", "type"]


class CreateUserRoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    custom_title = serializers.CharField(required=False)
    title = serializers.CharField(read_only=True)

    class Meta:
        model = Role
        fields = ["id", "title", "custom_title", "type"]

    def validate_custom_title(self, value):
        """Capitalize the custom title."""
        return value.capitalize()

    def validate(self, data):
        """Validate the input data."""
        role_id = data.get("id")
        custom_title = data.get("custom_title")

        if not Role.objects.filter(pk=role_id).exists() and not custom_title:
            raise serializers.ValidationError("Role does not exist.")
        if self._role_already_exists(role_id):
            raise serializers.ValidationError("You already have that role.")
        if not role_id and not custom_title:
            raise serializers.ValidationError(
                "Either 'role' or 'custom_title' must be provided."
            )
        if role_id and custom_title:
            raise serializers.ValidationError(
                "'Predefined role' and 'custom_title' cannot both be provided simultaneously."
            )
        if custom_title and self._custom_title_exists(custom_title):
            raise serializers.ValidationError(
                {
                    "duplicated": "A role with that title already exists, select from the list."
                }
            )

        return data

    def _role_already_exists(self, role_id):
        """Check if the role already exists for the user."""
        return role_id in [
            role.id for role in self.context.get("user_profile").roles.all()
        ]

    def _custom_title_exists(self, custom_title):
        """Check if a role with the custom title already exists."""
        return Role.objects.filter(title__iexact=custom_title).exists()

    def create(self, validated_data):
        """Create a new role or assign an existing one to the user profile."""
        with transaction.atomic():
            user_profile = self.context.get("user_profile")
            if not user_profile:
                raise ValidationError("User profile is required.")

            role_id = validated_data.get("id")
            custom_title = validated_data.get("custom_title")
            role_type = validated_data.get("type")

            if role_id:
                try:
                    user_role = Role.objects.get(id=role_id)
                except Role.DoesNotExist:
                    raise ValidationError(f"Role with id {role_id} does not exist.")

                user_profile.roles.add(user_role)
                user_profile.save()
            else:
                user_role = Role.objects.create(
                    title=custom_title, is_custom=True, type=role_type
                )
                user_profile.roles.add(user_role)
                user_profile.save()

            # Serialize the created/updated role and return the serialized data
            serialized_data = CreateUserRoleSerializer(user_role).data
            print(serialized_data)
            return serialized_data


class UserAreaSerializer(serializers.ModelSerializer):
    area = serializers.StringRelatedField()

    class Meta:
        model = UserArea
        fields = ["id", "area", "is_active"]


class CreateUserAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserArea
        fields = ["area"]

    def validate(self, data):
        area = data.get("area")
        if UserArea.objects.filter(
                user_profile=self.context.get("user_profile"), area=area
        ).exists():
            raise serializers.ValidationError(
                "This area of improvement is already set up by you,"
                " please choose another area"
            )
        return data

    def create(self, validated_data):
        user_profile = self.context.get("user_profile")
        if not user_profile:
            raise ValidationError("User profile is required.")

        user_area = UserArea.objects.create(
            user_profile_id=user_profile.id, area=validated_data.get("area")
        )

        return user_area


class UserGoalSerializer(serializers.ModelSerializer):
    goal = GoalSerializer()

    class Meta:
        model = UserGoal
        fields = [
            "id",
            "goal",
            "paused",
            "is_active",
            "progress",
            "goal_type",
            "is_completed",
            "due_date",
        ]


class EditUserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ["paused", "progress", "is_completed"]


class CreateUserGoalSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(
        queryset=Goal.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = UserGoal
        fields = ["id", "goal", "custom_goal", "goal_type", "due_date"]

    def validate(self, attr):
        if not attr.get("goal") and not attr.get("custom_goal"):
            raise serializers.ValidationError(
                "Either 'goal' or 'custom_goal' must be provided."
            )
        if UserGoal.objects.filter(
                user_profile=self.context.get("user_profile"), goal=attr.get("goal")
        ).exists():
            raise serializers.ValidationError(
                "This goal is already set up by you, please choose another goal or create"
                " a new one."
            )
        if Goal.objects.filter(title=attr.get('custom_goal')).exists():
            raise serializers.ValidationError(
                "This goal already exist, select from list"
            )
        return attr


class EditUserProfileSerializer(serializers.ModelSerializer):
    age_range = serializers.ChoiceField(choices=UserProfileChoices.AGE_RANGE_CHOICES, required=True)

    class Meta:
        model = UserProfile
        fields = [
            "name",
            "gender",
            "profile_image",
            "custom_gender",
            "age_range",
            "birth_date",
        ]

    def validate_birth_date(self, value):
        if value and value > datetime.date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value

    def validate(self, attrs):
        gender = attrs.get("gender")
        custom_gender = attrs.get("custom_gender")

        if gender == "Self describe" and not custom_gender:
            raise serializers.ValidationError(
                "Custom gender must be provided if you prefer to self-describe."
            )

        if gender != "Self describe" and custom_gender:
            raise serializers.ValidationError(
                "Custom gender should only be set when you prefer to self-describe."
            )

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "name",
            "gender",
            "profile_image",
            "custom_gender",
            "age_range",
        ]


class UserBalanceSerializer(serializers.ModelSerializer):
    life_sphere = serializers.CharField()

    class Meta:
        model = UserBalance
        fields = ["life_sphere", "score"]


class PrincipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principle
        fields = ['title', 'description']


class CreateUserPrincipleSerializer(serializers.ModelSerializer):
    principle_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserPrinciple
        fields = ["principle_id"]

    def validate(self, attrs):
        principle_id = attrs.get('principle_id')
        user_profile = self.context.get("user_profile")
        principle = get_object_or_404(Principle, id=principle_id)

        if UserPrinciple.objects.filter(user_profile=user_profile, principle=principle).exists():
            raise serializers.ValidationError({"error": "You have already adopted this principle."})
        return attrs

    def create(self, validated_data):
        principle_id = validated_data.pop('principle_id')
        user_profile_id = self.context.get('user_profile')
        principle = get_object_or_404(Principle, id=principle_id)
        instance = UserPrinciple.objects.create(user_profile=user_profile_id,
                                                principle=principle,
                                                **validated_data)
        return instance


class UserPrincipleSerializer(serializers.ModelSerializer):
    principle = PrincipleSerializer()

    class Meta:
        model = UserPrinciple
        fields = ['id', 'principle']
