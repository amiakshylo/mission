from django.urls import include, path
from user_management import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('user_profiles', views.UserProfileSet, basename='user_profiles')
urlpatterns = [
    path('', include(router.urls))
]