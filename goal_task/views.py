from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from silk.profiling.profiler import silk_profile

from goal_task.models import Goal, GoalSuggestionLog
from goal_task.openai.goal_suggestion_ai import generate_goal_with_openai
from goal_task.serializers import (
    GoalSuggestionInputSerializer,
    GoalSerializer,
)
from goal_task.services.text_utils import lemmatize_title, are_titles_similar, normalize_text


class GoalSuggestionsViewset(CreateModelMixin, GenericViewSet):
    """
    Viewset for goal suggestions.
    """

    serializer_class = GoalSuggestionInputSerializer
    queryset = Goal.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Create a new goal suggestion.
        """
        user_profile = request.user.user_profile
        roles_queryset = user_profile.roles.all()

        suggestion_serializer = self.get_serializer(data=request.data, context={"request": request})
        suggestion_serializer.fields["role"].queryset = roles_queryset

        if suggestion_serializer.is_valid():
            role = suggestion_serializer.validated_data["role"]
            top_n = self._get_top_n(request.data)

            suggested_goals = self.suggest_goals(user_profile, role, top_n=top_n)

            return Response(GoalSerializer(suggested_goals, many=True).data)

        return Response(suggestion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def suggest_goals(self, user_profile, role, top_n=5):
        """
        Suggest goals for a user based on their profile and role.
        """
        existing_goals = Goal.objects.filter(role=role)
        if existing_goals.count() < top_n:
            self._generate_goals_with_ai(user_profile, role, top_n - existing_goals.count())

        return Goal.objects.filter(role=role)[:top_n]

    def _generate_goals_with_ai(self, user_profile, role, count):
        """
        Generate goals using AI.
        """
        generated_goals = generate_goal_with_openai(user_profile, selected_role=role.title)
        if generated_goals:
            self.save_generated_goals(user_profile, generated_goals, role)

    def save_generated_goals(self, user_profile, generated_goals, role, source="openai"):
        """
        Save generated goals to the database.
        """
        created_goals = []
        logged_goals = []

        for goal_data in generated_goals:
            lemmatized_title = lemmatize_title(normalize_text(goal_data["title"]))
            existing_goals = Goal.objects.filter(role=role)
            is_duplicate = False

            for existing_goal in existing_goals:
                existing_lemmatized_title = lemmatize_title(normalize_text(existing_goal.title))

                if lemmatized_title == existing_lemmatized_title or are_titles_similar(lemmatized_title,
                                                                                       existing_lemmatized_title):
                    created_goals.append(existing_goal)
                    logged_goals.append(existing_goal)
                    is_duplicate = True
                    break

            if not is_duplicate:
                new_goal = Goal(
                    title=goal_data["title"],
                    description=goal_data["description"],
                    is_custom=True,
                )
                new_goal.save()
                new_goal.role.set([role])

                created_goals.append(new_goal)
                logged_goals.append(new_goal)

        GoalSuggestionLog.objects.bulk_create(
            [
                GoalSuggestionLog(
                    user_profile=user_profile,
                    goal=goal,
                    suggestion_source=source,
                    role=role,
                )
                for goal in logged_goals
            ]
        )

        return created_goals

    def _get_top_n(self, request_data):
        """
        Get the top N value from the request data.
        """
        top_n = request_data.get("top_n", 5)

        try:
            top_n = int(top_n)
        except ValueError:
            print(f"Invalid value for top_n: '{top_n}', defaulting to 5")
            top_n = 5

        return top_n


class GoalViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    List of all existing goals on the DB.
    Can be filtered by role ID because each role has own predefined goals.
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role']

    @silk_profile(name='Goals_profiler_list')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
