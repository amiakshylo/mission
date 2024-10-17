import torch
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from goal_task.ml.goal_suggestion_ml import (
    preprocess_user_data,
    reverse_goal_mapping,
    validate_model_output_size,
)
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
        unique_goals_count = Goal.objects.filter(role=role).distinct("id").count()

        if unique_goals_count < 50:
            self._generate_goals_with_ai(user_profile, role, unique_goals_count)

        return self.suggest_goals_with_ml(user_profile, role, top_n)

    def suggest_goals_with_ml(self, user_profile, role, top_n=5):
        """
        Suggest goals using a machine learning model.
        """
        model = validate_model_output_size()
        user_data_tensor = preprocess_user_data(user_profile, role)

        if user_data_tensor is not None:
            with torch.no_grad():
                prediction = model(user_data_tensor)
                top_n_indices = torch.topk(prediction, k=top_n, dim=1)[1]

                suggested_goals = self._get_suggested_goals(top_n_indices, role)

                if len(suggested_goals) < top_n:
                    additional_goals = Goal.objects.filter(role=role).exclude(
                        id__in=[goal.id for goal in suggested_goals])[: top_n - len(suggested_goals)]
                    suggested_goals.extend(additional_goals)

                return suggested_goals

        return self.generate_goal_with_openai_fallback(user_profile, role)

    def generate_goal_with_openai_fallback(self, user_profile, role):
        """
        Generate a goal using OpenAI as a fallback.
        """
        try:
            generated_goals = generate_goal_with_openai(user_profile, selected_role=role.title)
            if generated_goals:
                return self.save_generated_goals(user_profile, generated_goals, role)
        except Exception as e:
            print(f"OpenAI request failed: {e}")

        return Goal.objects.none()

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
                    created_by=user_profile.user,
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

    def _generate_goals_with_ai(self, user_profile, role, unique_goals_count):
        """
        Generate goals using AI until there are at least 50 unique goals.
        """
        while unique_goals_count < 50:
            generated_goals = generate_goal_with_openai(user_profile, selected_role=role.title)
            if generated_goals:
                new_goals = self.save_generated_goals(user_profile, generated_goals, role)
                unique_goals_count += len(new_goals)

    def _get_suggested_goals(self, top_n_indices, role):
        """
        Get the suggested goals based on the top N indices.
        """
        suggested_goals = []
        used_indices = set()

        for idx_tensor in top_n_indices[0]:
            idx = idx_tensor.item()
            if idx < Goal.objects.count() and idx not in used_indices:
                predicted_goal_id = reverse_goal_mapping(idx)
                goal = Goal.objects.filter(id=predicted_goal_id, role=role).first()
                if goal:
                    suggested_goals.append(goal)
                    used_indices.add(idx)
                else:
                    print(f"Predicted goal ID {predicted_goal_id} not found.")
            else:
                print(f"Predicted index {idx} is out of bounds for current goal count.")

        return suggested_goals
