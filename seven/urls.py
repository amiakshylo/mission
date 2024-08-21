import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_management.urls')),
    path('habit/', include('habit_management.urls')),
    path('', include('category_management.urls')),
    path('goal_task/', include('goal_task_management.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('auth/', include("djoser.urls")),
    path('journey/', include('journey.urls')),
    path("auth/", include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
