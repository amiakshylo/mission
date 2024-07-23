from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserProfileSerializer, EditUserProfileSerializer
from .models import UserProfile


class UserProfileSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = (UserProfile.objects.select_related('user').
                prefetch_related('user__user_roles').all())
    permission_classes = [IsAdminUser]

    def get_object(self):
        user_profile = UserProfile.objects.select_related('user').prefetch_related('user__user_roles',
                                                                                   'user__user_goals').get(
            user=self.request.user.id)
        return user_profile

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            serializer = UserProfileSerializer(self.get_object())
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


    @me.mapping.put
    def update_me(self, request):
        user_profile = self.get_object()
        serializer = EditUserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @me.mapping.delete
    def delete_me(self, request):
        user_profile = self.get_object()
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

