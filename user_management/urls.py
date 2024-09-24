from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("profile", views.UserProfileViewSet, basename="user_profile")
router.register("role", views.UserRoleViewSet, basename="user_role")
router.register("goal", views.UserGoalViewSet, basename="user_goal")
router.register("roles", views.RoleViewSet, basename="role")
router.register("area", views.UserAreaViewSet, basename="user_area")
router.register("balance", views.UserBalanceViewSet, basename="user_balance")

profile_image_router = routers.NestedDefaultRouter(
    router, "profile", lookup="user_profile"
)
profile_image_router.register("image", views.ImageProfileViewSet, basename="image")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(profile_image_router.urls)),
]
