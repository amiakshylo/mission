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
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),
    path('habit/', include('habit_management.urls')),
    path('', include('life_sphere.urls')),
    path('goal_task/', include('goal_task_management.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('auth/', include("djoser.urls")),
    path('journey/', include('journey.urls')),
    path("auth/", include("djoser.urls.jwt")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
