from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('user_profile', views.UserProfileSet, basename='user_profile')
router.register('user_role', views.UserRoleViewSet, basename='user_role')
router.register('user_goal', views.UserGoalViewSet, basename='user_goal')




# user_profiles_router = routers.NestedDefaultRouter(router, 'user_profile', lookup='user_profile')
# user_profiles_router.register('user_goal', views.UserGoalViewSet, basename='user_profile-user_goals')


urlpatterns = [
    path('', include(router.urls)),

    # path('', include(user_profiles_router.urls))
]