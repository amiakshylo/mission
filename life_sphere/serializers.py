from rest_framework import serializers
from .models import LifeSphere


class LifeSphereSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeSphere
        fields = ['id', 'title', 'description']
