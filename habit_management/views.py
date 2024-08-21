from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habit_management.models import Habit
from habit_management.serializers import UserHabitSerializer


class UserHabitViewSet(ModelViewSet):
    serializer_class = UserHabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user_profile=self.request.user.user_profile.id)
