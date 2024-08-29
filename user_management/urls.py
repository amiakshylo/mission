from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('user_profile', views.UserProfileSet, basename='user_profile')
router.register('user_role', views.UserRoleViewSet, basename='user_role')
router.register('user_goal', views.UserGoalViewSet, basename='user_goal')
router.register('role', views.RoleViewSet, basename='role')
router.register('user_area', views.UserAreaViewSet, basename='user_area')
router.register('user_balance', views.UserBalanceViewSet, basename='user_balance')

urlpatterns = [
    path('user/', include(router.urls)),
]
