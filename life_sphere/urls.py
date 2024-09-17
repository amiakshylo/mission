from django.urls import include, path
from rest_framework_nested import routers
from . import views

# Create the default router for life_spheres
router = routers.DefaultRouter()
router.register("", views.LifeSphereViewSet, basename="life-spheres")

# Create a nested router for areas within life_spheres
life_sphere_router = routers.NestedDefaultRouter(router, "", lookup="life_sphere")
life_sphere_router.register("area", views.AreaViewSet, basename="areas")

# Register both base and nested routes
urlpatterns = [
    path("", include(router.urls)),
    path("", include(life_sphere_router.urls)),
]
