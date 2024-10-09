from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.RoleModelViewSet, basename="principle")

# profile_router = routers.NestedDefaultRouter(router, "profile", lookup="user_profile")
# profile_router.register("role", views.UserRoleViewSet, basename="role")

urlpatterns = [
    path("", include(router.urls)),
]
