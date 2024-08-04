

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from goal_task_management.models import Goal
from category_management.models import SubCategory


from goal_task_management.serializers import GoalSerializer
from .models import UserProfile, UserRole, UserGoal

from .serializers import (UserProfileSerializer, EditUserProfileSerializer,

                          CreateUserRoleSerializer,
                          UserRoleSerializer, UserGoalSerializer, CreateUserGoalSerializer,
                          GoalSuggestionInputSerializer, GoalAutocompleteSerializer)


class UserProfileSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.select_related('user').all()
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT', 'DELETE'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_profile = get_object_or_404(
            UserProfile.objects.select_related('user').prefetch_related('user_habits', 'user_roles'),
            user=request.user
        )

        if self.request.method == 'GET':
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)

        if self.request.method == 'PUT':
            partial = request.method == 'PATCH'
            serializer = EditUserProfileSerializer(user_profile, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            changed_data = serializer.save()
            return Response(changed_data)

        if self.request.method == 'DELETE':
            user_profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserRoleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return UserRole.objects.prefetch_related('user_profiles').filter(user_profiles=user_profile).distinct()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserRoleSerializer
        return UserRoleSerializer

    def get_serializer_context(self):
        userprofile_pk = self.request.user.user_profile.id
        return {'user_profile_id': userprofile_pk}


class UserGoalViewSet(ModelViewSet):
    # logger = logging.getLogger('user_management')

    def get_serializer_class(self):
        if self.action == 'goal_suggestions_autocomplete':
            if self.request.method == 'POST':
                return GoalSuggestionInputSerializer
            else:
                return GoalAutocompleteSerializer
        if self.request.method in ['POST', 'PUT']:
            return CreateUserGoalSerializer
        return UserGoalSerializer

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return UserGoal.objects.filter(user_profile=user_profile)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_profile'] = self.request.user.user_profile
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_id = request.data.get('category')
        role_ids = request.data.getlist('role_ids')

        try:
            # Fetch the category and roles
            category = SubCategory.objects.get(id=category_id)
            roles = UserRole.objects.filter(id__in=role_ids)

            # Suggest goals based on the selected category and user's roles
            suggested_goals = Goal.objects.filter(category=category, roles__in=roles).distinct()

            if not suggested_goals.exists() and not serializer.validated_data.get('goal'):
                return Response({'error': 'No goals available for the selected category and roles.'}, status=status.HTTP_400_BAD_REQUEST)

            # If a goal is provided and valid, save it
            user_goal = serializer.save(user=request.user)
            return Response(UserGoalSerializer(user_goal).data, status=status.HTTP_201_CREATED)

        except SubCategory.DoesNotExist:
            return Response({'error': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='goal-suggestions-autocomplete')
    def goal_suggestions_autocomplete(self, request):
        # Step 1: Handle the goal suggestion based on category
        suggestion_serializer = GoalSuggestionInputSerializer(data=request.data, context={'request': request})
        suggestion_serializer.is_valid(raise_exception=True)

        category = suggestion_serializer.validated_data['category']
        user_profile = request.user.user_profile
        roles = UserRole.objects.filter(user_profiles=user_profile)

        # Step 2: Filter Goals based on the selected category and user's roles
        suggested_goals = Goal.objects.filter(sub_category=category, user_role__in=roles).distinct()

        # # Step 3: Handle custom goal query (if provided)
        # custom_goal_query = request.data.get('custom_goal', None)
        # if custom_goal_query:
        #     # Get AI-generated suggestions
        #     ai_suggestions = get_goal_suggestions(custom_goal_query)
        #     # Add AI suggestions to the existing suggested goals
        #     suggested_goals = ai_suggestions
        #
        # # Return the suggested goals (whether from the database or based on the query)
        # goal_serializer = GoalSerializer(suggested_goals, many=True)
        # return Response({'suggested_goals': goal_serializer.data}, status=status.HTTP_200_OK)

        # Step 3: Handle custom goal query (if provided)
        custom_goal_query = request.data.get('custom_goal', None)
        if custom_goal_query:
            autocomplete_serializer = GoalAutocompleteSerializer(data=request.data)
            autocomplete_serializer.is_valid(raise_exception=True)

            query = autocomplete_serializer.validated_data['custom_goal']
            query_words = query.split()  # Split the query into individual words

            # Create a Q object for each word in the query and combine them with AND logic
            query_filter = Q()
            for word in query_words:
                query_filter &= Q(title__icontains=word)

            suggested_goals = Goal.objects.filter(query_filter)

        # Return the suggested goals (whether from the database or based on the query)
        goal_serializer = GoalSerializer(suggested_goals, many=True)
        return Response({'suggested_goals': goal_serializer.data}, status=status.HTTP_200_OK)

