from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('user_profile', views.UserProfileSet, basename='user_profile')
router.register('user_role', views.UserRoleViewSet, basename='user_role')
router.register('user_goal', views.UserGoalViewSet, basename='user_goal')


urlpatterns = [
    path('', include(router.urls)),
]
