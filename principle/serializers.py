from rest_framework.serializers import ModelSerializer

from principle.models import RoleModel, Principle


class PrincipleSerializer(ModelSerializer):
    class Meta:
        model = Principle
        fields = ['id', "title", "description"]


class RoleModelSerializer(ModelSerializer):
    class Meta:
        model = RoleModel
        fields = ["id", "character_name", "description"]
