from django.urls import include, path
from user_management import views
from rest_framework_nested import routers

from user_management.views import OnboardingViewSet

router = routers.DefaultRouter()
router.register('user_profile', views.UserProfileSet, basename='user_profile')
router.register('onboarding', views.OnboardingViewSet, basename='onboarding')



user_profiles_router = routers.NestedDefaultRouter(router, 'user_profile', lookup='user_profile')
user_profiles_router.register('user_roles', views.UserRoleViewSet, basename='user_profile-user_roles')
user_profiles_router.register('user_goals', views.UserGoalViewSet, basename='user_profile-user_goals')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_profiles_router.urls))
]