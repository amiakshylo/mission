
import torch

from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from goal_task_management.ml.goal_suggestion_ml import (load_trained_model, preprocess_user_data,
                                                        train_pytorch_model,
                                                        get_output_size, reverse_goal_mapping,
                                                        validate_model_output_size)

from goal_task_management.models import Goal, GoalSuggestionLog
from goal_task_management.openai.goal_suggestion_ai import generate_goal_with_openai
from goal_task_management.serializers import GoalSuggestionInputSerializer, GoalSerializer
from utils.text_utils import lemmatize_title, are_titles_similar, normalize_text


class GoalSuggestionsViewset(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSuggestionInputSerializer
    queryset = Goal.objects.all()

    def create(self, request, *args, **kwargs):
        print("Starting goal suggestion process.")
        user_profile = request.user.user_profile
        roles_queryset = user_profile.roles.all()
        print(f"User Profile: {user_profile}, Roles: {[role.title for role in roles_queryset]}")

        suggestion_serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        suggestion_serializer.fields['role'].queryset = roles_queryset

        if suggestion_serializer.is_valid():
            role = suggestion_serializer.validated_data['role']
            print(f"Role selected: {role.title}")

            # Get the value of 'top_n' from the request data or default to 5
            top_n = request.data.get('top_n', 5)

            # Ensure that 'top_n' is an integer
            try:
                top_n = int(top_n)
            except ValueError:
                print(f"Invalid value for top_n: '{top_n}', defaulting to 5")
                top_n = 5

            suggested_goals = self.suggest_goals(user_profile, role, top_n=top_n)

            print(f"Returning {len(suggested_goals)} goals to the user.")
            return Response(GoalSerializer(suggested_goals, many=True).data)

        print("Suggestion serializer validation failed.")
        return Response(suggestion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def suggest_goals(self, user_profile, role, top_n=5):
        # Check the number of unique goals for the role
        unique_goals_count = Goal.objects.filter(role=role).distinct('id').count()
        print(f"Number of unique goals: {unique_goals_count}")

        if unique_goals_count < 50:  # Replace 50 with your desired threshold
            print(f"Less than 50 unique goals for role '{role.title}'. Generating goals with AI.")
            while unique_goals_count < 50:
                generated_goals = generate_goal_with_openai(user_profile, selected_role=role.title)
                if generated_goals:
                    # Save only unique goals
                    new_goals = self.save_generated_goals(user_profile, generated_goals, role)
                    unique_goals_count += len(new_goals)

        # Proceed with ML model suggestion if enough data
        return self.suggest_goals_with_ml(user_profile, role, top_n)

    def suggest_goals_with_ml(self, user_profile, role, top_n=5):
        model = validate_model_output_size()

        user_data_tensor = preprocess_user_data(user_profile, role)

        if user_data_tensor is not None:
            with torch.no_grad():
                prediction = model(user_data_tensor)
                top_n_indices = torch.topk(prediction, k=top_n, dim=1)[1]

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

                # If not enough goals are suggested, fill the rest with random goals
                if len(suggested_goals) < top_n:
                    additional_goals = Goal.objects.filter(role=role).exclude(
                        id__in=[goal.id for goal in suggested_goals])[:top_n - len(suggested_goals)]
                    suggested_goals.extend(additional_goals)

                return suggested_goals

        print("No valid user data for prediction. Using OpenAI fallback.")
        return self.generate_goal_with_openai_fallback(user_profile, role)

    def generate_goal_with_openai_fallback(self, user_profile, role):
        print("Attempting to generate a goal using OpenAI.")
        try:
            generated_goals = generate_goal_with_openai(user_profile, selected_role=role.title)
            if generated_goals:
                return self.save_generated_goals(user_profile, generated_goals, role)
        except Exception as e:
            print(f"OpenAI request failed: {e}")

        print("Returning an empty queryset as no goals were found or generated.")
        return Goal.objects.none()

    def save_generated_goals(self, user_profile, generated_goals, role, source='openai'):
        created_goals = []
        logged_goals = []

        for goal_data in generated_goals:
            # Normalize and lemmatize the title
            lemmatized_title = lemmatize_title(normalize_text(goal_data['title']))

            # Check against all existing goals for the role
            existing_goals = Goal.objects.filter(role=role)
            is_duplicate = False

            for existing_goal in existing_goals:
                existing_lemmatized_title = lemmatize_title(normalize_text(existing_goal.title))

                if lemmatized_title == existing_lemmatized_title or are_titles_similar(lemmatized_title, existing_lemmatized_title):
                    print(f"Similar goal found: '{lemmatized_title}', not saving.")
                    created_goals.append(existing_goal)  # Add existing goal to the list
                    logged_goals.append(existing_goal)  # Track for logging
                    is_duplicate = True
                    break

            if not is_duplicate:
                # Create and save a new goal with the original title and description
                new_goal = Goal(
                    title=goal_data['title'],
                    description=goal_data['description'],
                    is_custom=True,
                    created_by=user_profile.user
                )
                new_goal.save()  # Save individually to get an ID
                new_goal.role.set([role])  # Assign role after saving

                created_goals.append(new_goal)
                logged_goals.append(new_goal)

        # Log all suggestions, including duplicates
        GoalSuggestionLog.objects.bulk_create([
            GoalSuggestionLog(user_profile=user_profile, goal=goal, suggestion_source=source, role=role)
            for goal in logged_goals
        ])

        # Return all the goals, including those that weren't saved again because they were duplicates
        return created_goals
