# from datetime import datetime, date

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from goal_task_management.models import Goal
from goal_task_management.serializers import GoalSerializer
from .models import UserProfile, UserRole, UserGoal

from .serializers import (UserProfileSerializer, EditUserProfileSerializer,

                          CreateUserRoleSerializer,
                          UserRoleSerializer, UserGoalSerializer, CreateUserGoalSerializer)


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
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def suggest_goals(self, request):
        user_profile = request.user.user_profile
        selected_roles = user_profile.user_roles.all()

        selected_categories = request.query_params.getlist('categories')
        if not selected_categories:
            return Response({'categories': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        goals = Goal.objects.filter(user_role__id=1, sub_category__id=4).distinct()
        print(goals)

        suggested_goals = Goal.objects.filter(
            user_role__in=selected_roles,  # Filter by roles
            sub_category__id__in=selected_categories  # Filter by selected categories
        ).distinct()




        # Serialize and return the suggested goals
        serializer = GoalSerializer(suggested_goals, many=True)
        return Response(serializer.data)


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserGoalSerializer
        return UserGoalSerializer

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return UserGoal.objects.filter(user_profile=user_profile)

    def get_serializer_context(self):
        userprofile_pk = self.request.user.user_profile.id
        return {'user_profile_id': userprofile_pk}
