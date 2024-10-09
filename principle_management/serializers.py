from rest_framework.serializers import ModelSerializer

from principle_management.models import RoleModel, Principle


class PrincipleSerializer(ModelSerializer):
    class Meya:
        model = Principle
        fields = ["title", "description"]


class RoleModelSerializer(ModelSerializer):
    class Meta:
        model = RoleModel
        fields = ["id", "character_name", "description"]
