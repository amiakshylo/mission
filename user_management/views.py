from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from goal_task_management.models import Goal

from .models import UserProfile, UserGoal
from .serializers import (UserProfileSerializer, EditUserProfileSerializer,

                          CreateUserRoleSerializer,
                          UserRoleSerializer, UserGoalSerializer, CreateUserGoalSerializer,
                          EditUserGoalSerializer)


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
        return user_profile.roles.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserRoleSerializer
        return UserRoleSerializer

    def get_serializer_context(self):
        userprofile_pk = self.request.user.user_profile.id
        return {'user_profile_id': userprofile_pk}


class UserGoalViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['goal_type', 'is_active', 'is_completed']

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return CreateUserGoalSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return EditUserGoalSerializer
        return UserGoalSerializer

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return user_profile.goals.prefetch_related('goal')

    def get_serializer_context(self, *args, **kwargs):
        user_profile = self.request.user.user_profile.id
        return {'user_profile': user_profile}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = request.user.user_profile
        goal = serializer.validated_data.get('goal')
        custom_goal_title = serializer.validated_data.get('custom_goal')
        category = serializer.validated_data.get('category')
        goal_type = serializer.validated_data.get('goal_type')
        due_date = serializer.validated_data.get('due_date')

        with transaction.atomic():
            if custom_goal_title:
                # Create a new Goal if it's a custom goal
                goal = Goal.objects.create(
                    sub_category=category,
                    title=custom_goal_title,
                    description=custom_goal_title,
                    due_date=due_date,
                    is_custom=True,
                    created_by=request.user,

                )

            # Create the UserGoal record
            user_goal = UserGoal.objects.create(user_profile=user_profile, goal=goal, goal_type=goal_type, due_date=due_date, **kwargs)

        return Response(UserGoalSerializer(user_goal).data, status=status.HTTP_201_CREATED)
