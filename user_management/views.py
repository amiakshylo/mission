import os.path
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter
from goal_task_management.models import Goal
from .filters import RoleFilter, UserAreaFilter
from .models import UserProfile, UserGoal, Role, UserArea, UserBalance, UserProfileImage
from .pagination import DefaultPagination
from .serializers import (
    UserProfileSerializer,
    EditUserProfileSerializer,
    CreateUserRoleSerializer,
    UserRoleSerializer,
    UserGoalSerializer,
    CreateUserGoalSerializer,
    EditUserGoalSerializer,
    RoleSerializer,
    UserAreaSerializer,
    CreateUserAreaSerializer,
    UserBalanceSerializer,
    UserImageProfileSerializer,
)


class UserProfileViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):

    def get_queryset(self):
        user_id = self.request.user
        return UserProfile.objects.filter(user=user_id).select_related("user")

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return EditUserProfileSerializer
        return UserProfileSerializer


class UserProfileImageViewSet(ModelViewSet):
    serializer_class = UserImageProfileSerializer

    def get_queryset(self):
        user_profile_pk = self.request.user.user_profile.id
        return UserProfileImage.objects.filter(user_profile=user_profile_pk)

    def create(self, request, *args, **kwargs):
        user_profile = self.kwargs.get("user_profile_pk")

        serializer = self.get_serializer(
            data=request.data, context={"user_profile_id": user_profile}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        profile_image = instance.profile_image

        if profile_image:
            image_path = profile_image.path

            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                    instance.delete()
                    return Response(
                        "Image deleted successfully", status=status.HTTP_204_NO_CONTENT
                    )
                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    "Image file does not exist", status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            "No image associated with this profile", status=status.HTTP_404_NOT_FOUND
        )


class RoleViewSet(ListModelMixin, GenericViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = RoleFilter
    search_fields = ["title"]


class UserRoleViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):

    def get_queryset(self):
        user_profile = self.request.user.user_profile

        return Role.objects.filter(user_profile=user_profile)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserRoleSerializer
        return UserRoleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user_profile"] = self.request.user.user_profile
        return context

    def destroy(self, request, *args, **kwargs):
        user_profile = self.request.user.user_profile
        role = self.get_object()

        user_profile.roles.remove(role)

        return Response(
            {"detail": "Role removed from profile."}, status=status.HTTP_204_NO_CONTENT
        )


class UserGoalViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["goal_type", "is_active", "is_completed"]

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return CreateUserGoalSerializer
        if self.request.method in ["PUT", "PATCH"]:
            return EditUserGoalSerializer
        return UserGoalSerializer

    def get_queryset(self):
        user_profile = self.request.user.user_profiley
        return user_profile.goals.prefetch_related("goal")

    def get_serializer_context(self, *args, **kwargs):
        user_profile = self.request.user.user_profile.id
        return {"user_profile": user_profile}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_profile = request.user.user_profile
        goal = serializer.validated_data.get("goal")
        custom_goal_title = serializer.validated_data.get("custom_goal")
        category = serializer.validated_data.get("category")
        goal_type = serializer.validated_data.get("goal_type")
        due_date = serializer.validated_data.get("due_date")

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
            user_goal = UserGoal.objects.create(
                user_profile=user_profile,
                goal=goal,
                goal_type=goal_type,
                due_date=due_date,
                **kwargs
            )

        return Response(
            UserGoalSerializer(user_goal).data, status=status.HTTP_201_CREATED
        )


class UserAreaViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAreaFilter

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return UserArea.objects.filter(user_profile=user_profile).select_related('area__life_sphere')


    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserAreaSerializer
        return UserAreaSerializer

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile

        return {"user_profile": user_profile}


class UserBalanceViewSet(ListModelMixin, GenericViewSet):
    queryset = UserBalance.objects.select_related("user_profile").prefetch_related(
        "life_sphere"
    )
    serializer_class = UserBalanceSerializer
