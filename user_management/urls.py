from django.urls import include, path
from user_management import views
from rest_framework_nested import routers

from user_management.views import OnboardingViewSet

router = routers.DefaultRouter()
router.register('user_profiles', views.UserProfileSet, basename='user_profiles')
router.register('onboarding', views.OnboardingViewSet, basename='onboarding')
urlpatterns = [
    path('', include(router.urls)),
]