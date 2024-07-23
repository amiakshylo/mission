from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User, UserProfile, UserRole, UserGoal


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('email', 'password')


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'username']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    current_habits = serializers.CharField(read_only=True)
    user_role = serializers.SerializerMethodField()
    user_goal = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'gender', 'location', 'profile_picture', 'ai_assistant_model', 'birth_date',
                  'current_habits', 'dashboard_customization', 'notification_preferences', 'user_role', 'user_goal']

    def get_user_role(self, obj):
        roles = obj.user.user_roles.all()  # Fetch all roles related to the user
        roles_list = []
        for role in roles:
            if role.is_custom:
                roles_list.append(role.custom_title)
            elif role.predefined_role:
                roles_list.append(role.predefined_role.title)
            else:
                roles_list.append('Custom Role')  # Fallback title
        return roles_list

    def get_user_goal(self, obj):
        gols = obj.user.user_goals.all()
        gols_list = []
        for goal in gols:
            if goal.is_custom:
                gols_list.append(goal.custom_title)

            elif goal.predefined_goal:
                gols_list.append(goal.predefined_goal.title)

            else:
                gols_list.append('Custom Goal')
        return gols_list


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'gender', 'location', 'profile_picture', 'ai_assistant_model', 'birth_date',
                  'dashboard_customization', 'notification_preferences']

