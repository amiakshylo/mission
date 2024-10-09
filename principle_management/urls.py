from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("rolemodel", views.RoleModelViewSet, basename="rolemodel")
router.register("principle", views.PrincipleViewSet, basename='principle')

rolemodel_router = routers.NestedDefaultRouter(router, "rolemodel", lookup="rolemodel")
rolemodel_router.register("principle", views.PrincipleViewSet, basename="rolemodel-principles")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(rolemodel_router.urls))
]
