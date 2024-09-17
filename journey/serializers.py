from rest_framework import serializers

from journey.models import (
    Journey,
    JourneyStep,
    UserJourneyStatus,
    UserJourneyStepStatus,
)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = ["id", "title", "description"]


class JourneyStepSerializer(serializers.ModelSerializer):
    journey = serializers.StringRelatedField()

    class Meta:
        model = JourneyStep
        fields = ["id", "title", "description", "journey"]


class StartJourneyStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyStep
        fields = ["id"]


class UserJourneyStepStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserJourneyStepStatus
        fields = ["started_at", "ended_at", "paused"]


class UserJourneyStatusSerializer(serializers.ModelSerializer):
    journey = serializers.StringRelatedField()
    current_step = serializers.StringRelatedField()
    step_status = serializers.SerializerMethodField()

    class Meta:
        model = UserJourneyStatus
        fields = [
            "user_profile",
            "journey",
            "current_step",
            "step_status",
            "started_at",
            "progress",
            "ended_at",
            "paused",
        ]

    def get_step_status(self, obj):
        user_profile = obj.user_profile
        current_step = obj.current_step

        # Fetch the UserJourneyStepStatus for the current step and user
        step_status = UserJourneyStepStatus.objects.filter(
            user_profile=user_profile, step=current_step
        ).first()

        # If a step status exists, return serialized data, else return None
        if step_status:
            return UserJourneyStepStatusSerializer(step_status).data
        return {}
