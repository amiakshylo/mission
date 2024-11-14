from django.urls import include, path
from rest_framework_nested import routers

from user_management import views

router = routers.DefaultRouter()
router.register("profiles", views.UserProfileViewSet, basename="profile")
router.register("goals", views.UserGoalViewSet, basename="goal")
router.register("roles", views.UserRoleViewSet, basename="role")
router.register("areas", views.UserAreaViewSet, basename="area")
router.register("balances", views.UserBalanceViewSet, basename="balance")
router.register("principles", views.UserPrincipleViewSet, basename='principle')

urlpatterns = [
    path("", include(router.urls)),
]
