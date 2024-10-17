from django.urls import include, path
from rest_framework_nested import routers

from role import views

router = routers.DefaultRouter()
router.register("", views.RoleViewSet, basename='role-list')

urlpatterns = [
    path("", include(router.urls)),
]
