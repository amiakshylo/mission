from rest_framework import serializers
from .models import Habit


class UserHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'title')
