from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from goal_task.models import Goal
from goal_task.serializers import (
    GoalSerializer, GoalSuggestionSerializer,
)
from goal_task.services.goal_suggestion_services import GoalSuggestionService


class GoalSuggestionsViewset(CreateModelMixin, GenericViewSet):
    """
    Viewset for goal suggestions. Returns all goals related to the chosen role.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSuggestionSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new goal suggestion and return all goals related to the selected role.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        role = serializer.validated_data["role"]
        user_profile = request.user.user_profile

        goal_suggestion_service = GoalSuggestionService(user_profile, role)
        suggested_goals = goal_suggestion_service.suggest_goals()

        return Response(GoalSerializer(suggested_goals, many=True).data, status=status.HTTP_200_OK)


class GoalViewSet(ListModelMixin, GenericViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']
