from datetime import datetime, date

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from .models import UserProfile, OnboardingStep, UserOnboardingStatus, UserRole, UserGoal, PredefinedRole, \
    PredefinedGoal
from .serializers import (UserProfileSerializer, EditUserProfileSerializer, OnboardingStepSerializer,
                          OnboardingStep2Serializer, OnboardingStep3Serializer,
                          OnboardingStep4Serializer, CreateUserRoleSerializer, PredefinedRoleSerializer,
                          PredefinedGoalSerializer, UserRoleSerializer)


class UserProfileSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = UserProfileSerializer
    queryset = (UserProfile.objects.select_related('user').
                prefetch_related('roles__role', 'goals').
                all())
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT', 'DELETE'], permission_classes=[IsAuthenticated])
    def me(self, request):
        queryset = UserProfile.objects.select_related('user').prefetch_related('roles__role', 'goals')
        user_profile = get_object_or_404(queryset, user=request.user)
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


class OnboardingViewSet(ModelViewSet):
    queryset = OnboardingStep.objects.all()
    serializer_class = OnboardingStepSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['get'])
    def steps(self, request):
        steps = OnboardingStep.objects.all()
        serializer = OnboardingStepSerializer(steps, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='predefined-roles')
    def predefined_roles(self, request):
        predefined_roles = PredefinedRole.objects.all()
        serializer = PredefinedRoleSerializer(predefined_roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='step2', serializer_class=OnboardingStep2Serializer)
    def onboarding_step2(self, request):
        user = request.user
        data = request.data

        birth_date_str = data.get('birth_date', None)
        if birth_date_str in [None, '', '“”']:
            return Response({'birth_date': ["This field is required and must be in YYYY-MM-DD format."]},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
            if birth_date > date.today():
                return Response({'birth_date': ["Birth date cannot be in the future."]},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'birth_date': ["Birth date must be in YYYY-MM-DD format."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # Proceed with the original logic if birth_date is valid
        onboarding_status = get_object_or_404(UserOnboardingStatus, user=user)
        onboarding_status.current_step = OnboardingStep.objects.get(step_number=2)
        onboarding_status.save()

        user_profile = get_object_or_404(UserProfile, user=user)
        user_profile.birth_date = birth_date
        user_profile.save()

        return Response({"message": "Step 2 completed successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='step3', serializer_class=OnboardingStep3Serializer)
    def onboarding_step3(self, request):
        user = request.user
        data = request.data

        # Validate and save step 3 data
        onboarding_status = get_object_or_404(UserOnboardingStatus, user=user)
        onboarding_status.current_step = OnboardingStep.objects.get(step_number=3)
        onboarding_status.save()

        user_profile = get_object_or_404(UserProfile, user=user)
        roles = data.get('roles', [])
        custom_roles = data.get('custom_roles', [])

        # Assign predefined roles
        if roles:
            predefined_roles = PredefinedRole.objects.filter(id__in=roles)
            user_profile.roles.clear()
            for role in predefined_roles:
                user_role = UserRole.objects.create(predefined_role=role, is_custom=False)
                user_profile.roles.add(user_role)

        # Create and assign custom roles
        for custom_role in custom_roles:
            user_role = UserRole.objects.create(
                custom_title=custom_role.get('custom_title'),
                custom_group=custom_role.get('custom_group'),
                is_custom=True
            )
            user_profile.roles.add(user_role)

        user_profile.save()

        return Response({"message": "Step 3 completed successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='suggested-goals')
    def suggested_goals(self, request):
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        user_roles = user_profile.roles.all()
        predefined_roles = PredefinedRole.objects.filter(user_roles__in=user_roles)
        suggested_goals = PredefinedGoal.objects.filter(roles__in=predefined_roles).distinct()
        serializer = PredefinedGoalSerializer(suggested_goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='step4', serializer_class=OnboardingStep4Serializer)
    def onboarding_step4(self, request):
        user = request.user
        data = request.data

        # Validate and save step 4 data
        onboarding_status = get_object_or_404(UserOnboardingStatus, user=user)
        onboarding_status.current_step = OnboardingStep.objects.get(step_number=4)
        onboarding_status.is_completed = True
        onboarding_status.save()

        user_profile = get_object_or_404(UserProfile, user=user)
        goals = data.get('goals', [])
        custom_goals = data.get('custom_goals', [])

        # Assign predefined goals
        if goals:
            predefined_goals = PredefinedGoal.objects.filter(id__in=goals)
            user_profile.goals.clear()
            for goal in predefined_goals:
                user_goal = UserGoal.objects.create(predefined_goal=goal, is_custom=False)
                user_profile.goals.add(user_goal)

        # Get existing user goal titles to avoid duplicates
        existing_goal_titles = set(
            user_profile.goals.values_list('custom_title', flat=True)
        )
        predefined_goal_titles = set(
            PredefinedGoal.objects.values_list('title', flat=True)
        )

        # Create and assign custom goals, avoiding duplicates
        for custom_goal in custom_goals:
            custom_title = custom_goal.get('custom_title')
            custom_description = custom_goal.get('custom_description')

            if custom_title and custom_title not in existing_goal_titles and custom_title not in predefined_goal_titles:
                user_goal = UserGoal.objects.create(
                    custom_title=custom_title,
                    custom_description=custom_description,
                    is_custom=True
                )
                user_profile.goals.add(user_goal)
                existing_goal_titles.add(custom_title)  # Add to the set to avoid duplicates

        user_profile.save()

        return Response({"message": "Step 4 completed successfully and onboarding completed"},
                        status=status.HTTP_200_OK)


class UserRoleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateUserRoleSerializer
        return UserRoleSerializer

    def get_queryset(self):
        current_user = self.request.user.id
        requested_user = self.kwargs.get('user_profile_pk')
        if int(requested_user) == current_user:
            roles = UserRole.objects.filter(user_profiles=current_user).select_related('role').all()
            return roles
        else:
            raise PermissionDenied("You do not have permission to view this user's roles.")

    def get_serializer_context(self):
        userprofile_pk = self.kwargs['user_profile_pk']
        return {'user_profile_id': userprofile_pk}

