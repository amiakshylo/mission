from rest_framework import serializers
from .models import LifeSphere, Area


class LifeSphereSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeSphere
        fields = ["id", "title", "description"]


class AreaSerializer(serializers.ModelSerializer):
    life_sphere = serializers.StringRelatedField()

    class Meta:
        model = Area
        fields = ["id", "title", "description", "life_sphere"]


class AddUserAreaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Area
        fields = ["id"]


