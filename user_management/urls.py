from django.urls import include, path
from rest_framework_nested import routers

from user_management import views

router = routers.DefaultRouter()
router.register("profile", views.UserProfileViewSet, basename="user_profile")
router.register("goal", views.UserGoalViewSet, basename="user_goal")
router.register("role", views.UserRoleViewSet, basename="role")
router.register("area", views.UserAreaViewSet, basename="user_area")
router.register("balance", views.UserBalanceViewSet, basename="user_balance")
router.register("principle", views.UserPrincipleViewSet, basename='user_principle')

urlpatterns = [
    path("", include(router.urls)),
]
