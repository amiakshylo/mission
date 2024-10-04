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


class MinimalJourneyStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyStep
        fields = ['step_number', 'title']


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
    current_step = MinimalJourneyStepSerializer(read_only=True)

    class Meta:
        model = UserJourneyStatus
        fields = [
            'journey',
            'started_at',
            'is_completed',
            'completed_steps',
            'current_step'
        ]


class UserJourneyStartSerializer(serializers.ModelSerializer):
    journey = serializers.StringRelatedField

    class Meta:
        model = UserJourneyStatus
        fields = ['journey', 'started_at']


class NextStepSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserJourneyStatus
        fields = ['id']



