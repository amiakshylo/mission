from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_management.urls')),
    path('habit/', include('habit_management.urls')),
    path('gth/', include('goal_task_management.urls')),
    path('category_management/', include('category_management.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('auth/', include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
