from rest_framework import serializers

from goal_task.models import Goal
from user_management.models import Role


class GoalSerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField()

    class Meta:
        model = Goal
        fields = ["id", "title", "description", "sub_category"]


class GoalSuggestionSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=True)
    search = serializers.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(GoalSuggestionSerializer, self).__init__(*args, **kwargs)
        self.fields["role"].queryset = kwargs["context"][
            "request"
        ].user.user_profile.roles.all()

    class Meta:
        model = Role
        fields = ["role", "search"]
