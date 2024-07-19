from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_management.urls')),
    path('gth/', include('goal_task_habit.urls')),
    path('category/', include('category.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
