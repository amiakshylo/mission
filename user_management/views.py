from django.db import transaction
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, DestroyModelMixin, CreateModelMixin

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter

from life_sphere.models import LifeSphere
from goal_task_management.models import Goal
from .filters import RoleFilter

from .models import UserProfile, UserGoal, Role, UserArea, UserBalance
from .pagination import DefaultPagination
from .serializers import (UserProfileSerializer, EditUserProfileSerializer,

                          CreateUserRoleSerializer,
                          UserRoleSerializer, UserGoalSerializer, CreateUserGoalSerializer,
                          EditUserGoalSerializer, RoleSerializer, UserAreaSerializer, CreateUserAreaSerializer,
                          UserBalanceSerializer)


class UserProfileSet(ListModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return UserProfile.objects.all().select_related('user')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        queryset = UserProfile.objects.all().select_related('user').prefetch_related('roles')
        user_profile = get_object_or_404(queryset, user=request.user)

        if request.method == 'PUT':
            serializer = EditUserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)


# ATTENTION REDUNDANT QUERIES >

class RoleViewSet(ListModelMixin, GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RoleFilter
    search_fields = ['title']


class UserRoleViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.user_profile

        return Role.objects.filter(user_profile=user_profile)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserRoleSerializer
        return UserRoleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_profile'] = self.request.user.user_profile
        return context

    def destroy(self, request, *args, **kwargs):
        user_profile = self.request.user.user_profile
        role = self.get_object()

        # Remove the role from the user's profile without deleting the role
        user_profile.roles.remove(role)

        # Return a response indicating success
        return Response({"detail": "Role removed from profile."}, status=status.HTTP_204_NO_CONTENT)


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
            user_goal = UserGoal.objects.create(user_profile=user_profile, goal=goal, goal_type=goal_type,
                                                due_date=due_date, **kwargs)

        return Response(UserGoalSerializer(user_goal).data, status=status.HTTP_201_CREATED)


class UserAreaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserArea.objects.filter(user_profile=self.request.user.user_profile)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserAreaSerializer
        return UserAreaSerializer

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        print(user_profile)

        return {'user_profile': user_profile}


class UserBalanceViewSet(ListModelMixin, GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = UserBalanceSerializer

    def get_queryset(self):
        return UserBalance.objects.filter(user_profile=self.request.user.user_profile)


