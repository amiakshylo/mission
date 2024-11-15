from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from user_management.tasks import notify_customers
from .filters import UserAreaFilter
from .models import Role, UserArea, UserBalance, UserPrinciple, UserGoal, UserProfile
from .pagination import DefaultPagination
from .serializers import (
    UserProfileSerializer,
    EditUserProfileSerializer,
    CreateUserRoleSerializer,
    UserRoleSerializer,
    UserGoalSerializer,
    CreateUserGoalSerializer,
    EditUserGoalSerializer,
    UserAreaSerializer,
    CreateUserAreaSerializer,
    UserBalanceSerializer, CreateUserPrincipleSerializer, UserPrincipleSerializer,
)


class UserProfileViewSet(ListModelMixin,
                         UpdateModelMixin, GenericViewSet
                         ):
    def get_queryset(self):
        user_profile = self.request.user.user_profile.id
        return UserProfile.objects.filter(id=user_profile).select_related('user')

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return EditUserProfileSerializer
        return UserProfileSerializer


class UserRoleViewSet(
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):

    def get_queryset(self):
        notify_customers.delay('Hello')
        user_profile = self.request.user.user_profile

        return Role.objects.filter(user_profile=user_profile)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserRoleSerializer
        return UserRoleSerializer

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        return {"user_profile": user_profile}

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
    pagination_class = DefaultPagination

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return CreateUserGoalSerializer
        if self.request.method in ["PUT", "PATCH"]:
            return EditUserGoalSerializer
        return UserGoalSerializer

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return user_profile.goals.prefetch_related('goal')

    def get_serializer_context(self, *args, **kwargs):
        user_profile = self.request.user.user_profile.id
        return {"user_profile": user_profile}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_goal = UserGoal.create_user_goal(
            user_profile=self.request.user.user_profile,
            validated_data=serializer.validated_data
        )
        return Response(UserGoalSerializer(user_goal).data, status=status.HTTP_201_CREATED)


class UserAreaViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAreaFilter

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return UserArea.objects.filter(user_profile=user_profile).select_related(
            "area__life_sphere"
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserAreaSerializer
        return UserAreaSerializer

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        return {"user_profile": user_profile}


class UserBalanceViewSet(ListModelMixin, GenericViewSet):
    serializer_class = UserBalanceSerializer

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return UserBalance.objects.filter(user_profile=user_profile).select_related("user_profile").prefetch_related(
            "life_sphere"
        )


class UserPrincipleViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserPrincipleSerializer
        return UserPrincipleSerializer

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return UserPrinciple.objects.filter(user_profile=user_profile).prefetch_related('principle')

    def get_serializer_context(self):
        user_profile = self.request.user.user_profile
        return {"user_profile": user_profile}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = self.get_serializer(instance)

        return Response(
            {
                "message": f"You successfully adopted principle: {instance.principle.title}",
            },
            status=status.HTTP_201_CREATED
        )
