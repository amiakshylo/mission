import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Mission",
        default_version="v1",
        description="API documentation for Mission project",
        contact=openapi.Contact(email="andrew.m@evolvion.tech"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # jwt urls
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("__debug__/", include(debug_toolbar.urls)),
    # app urls
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("user_management.urls")),
    path("api/v1/role/", include("role.urls")),
    path("api/v1/principle/", include("principle.urls")),
    path("api/v1/life_sphere/", include("life_sphere.urls")),
    path("api/v1/goal_task/", include("goal_task.urls")),
    path("api/v1/journey/", include("journey.urls")),
    path("api/v1/onboarding/", include("onboarding.urls")),

    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "swagger.yaml/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),  # OpenAPI schema in JSON format
    path(
        "swagger.json/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),  # OpenAPI schema in YAML format

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
