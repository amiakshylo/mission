from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity, SearchRank
from django.db.models import Q

from rest_framework import status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from goal_task_management.openai.integration import generate_goal_with_openai
from goal_task_management.ml.goal_suggestion_model import train_model, predict_goal
from goal_task_management.models import Goal, GoalSuggestionLog
from goal_task_management.serializers import GoalSuggestionInputSerializer, GoalSerializer
from user_management.models import UserGoal


class GoalSuggestionsViewset(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSuggestionInputSerializer
    queryset = Goal.objects.all()

    def create(self, request, *args, **kwargs):
        print("Starting goal suggestion process.")
        user_profile = request.user.user_profile
        roles_queryset = user_profile.roles.all()
        print(f"User Profile: {user_profile}, Roles: {[role.title for role in roles_queryset]}")

        # Initialize the serializer with the filtered queryset directly
        suggestion_serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        suggestion_serializer.fields['role'].queryset = roles_queryset

        if suggestion_serializer.is_valid():
            role = suggestion_serializer.validated_data['role']
            print(f"Role selected: {role.title}")

            # Step 1: Train or load the ML model
            model = self.load_model()

            if model:
                # Step 2: Predict a goal using the ML model
                predicted_goal_id = self.predict_goal_with_logging(model, user_profile)
                suggested_goals = Goal.objects.filter(id=predicted_goal_id)
                print(f"Predicted goal ID: {predicted_goal_id}")
            else:
                # Fallback to your existing logic if no model or prediction available
                print("Model loading failed or not available. Using fallback logic.")
                suggested_goals = Goal.objects.filter(role=role)

            # Perform search filtering if a search query is provided
            search_query = request.data.get('search', None)
            if search_query:
                print(f"Search query received: {search_query}")
                suggested_goals = self.search_goals(suggested_goals, search_query)
                print(f"Search filtering applied. {suggested_goals.count()} goals found.")

            # If no suggested goals were found, fallback to OpenAI
            if not suggested_goals.exists():
                print("No goals found. Falling back to OpenAI.")
                suggested_goals = self.generate_goal_with_openai_fallback(user_profile, role)

            print(f"Returning {suggested_goals.count()} goals to the user.")
            return Response(GoalSerializer(suggested_goals, many=True).data)

        print("Suggestion serializer validation failed.")
        return Response(suggestion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def load_model(self):
        print("Loading the ML model.")
        try:
            model = train_model()
            print("Model loaded successfully.")
            return model
        except Exception as e:
            print(f"Error loading or training model: {e}")
            return None

    def predict_goal_with_logging(self, model, user_profile):
        print("Predicting goal using the ML model.")
        try:
            predicted_goal_id = predict_goal(model, user_profile)
            print(f"Prediction successful. Goal ID: {predicted_goal_id}")
            return predicted_goal_id
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None

    def search_goals(self, queryset, search_query):
        print("Applying search filtering on goals.")
        try:
            # Creating a custom search vector for title and description
            vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            query = SearchQuery(search_query, search_type='websearch')

            # Annotate the queryset with rank and trigram similarity
            filtered_queryset = queryset.annotate(
                rank=SearchRank(vector, query),
                trigram_similarity=TrigramSimilarity('title', search_query)
            ).filter(
                Q(rank__gte=0.2) | Q(trigram_similarity__gt=0.2)
            ).distinct().order_by('-rank', '-trigram_similarity')

            print(f"Search completed. {filtered_queryset.count()} goals matched.")
            return filtered_queryset
        except Exception as e:
            print(f"Error during search filtering: {e}")
            return queryset

    def generate_goal_with_openai_fallback(self, user_profile, role):
        print("Attempting to generate a goal using OpenAI.")
        try:
            generated_goal = generate_goal_with_openai(user_profile, selected_role=role.title)
            if generated_goal:
                print(f"OpenAI generated a goal: {generated_goal['title']}")
                goal = Goal.objects.create(
                    title=generated_goal['title'],
                    description=generated_goal['description'],
                    is_custom=True,
                    created_by=user_profile.user,
                )
                GoalSuggestionLog.objects.create(user_profile=user_profile, goal=goal, suggestion_source='openai')
                return Goal.objects.filter(id=goal.id)
            else:
                print("OpenAI did not return a goal.")
        except Exception as e:
            print(f"OpenAI request failed: {e}")

        print("Returning an empty queryset as no goals were found or generated.")
        return Goal.objects.none()