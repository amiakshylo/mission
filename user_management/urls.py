from django.urls import include, path

from . import views
from rest_framework_nested import routers



router = routers.DefaultRouter()
router.register('user_profile', views.UserProfileSet, basename='user_profile')
router.register('user_role', views.UserRoleViewSet, basename='user_role')
router.register('user_goal', views.UserGoalViewSet, basename='user_goal')




# user_profiles_router = routers.NestedDefaultRouter(router, 'user_profile', lookup='user_profile')
# user_profiles_router.register('user_goal', views.UserGoalViewSet, basename='user_profile-user_goals')


urlpatterns = [
    path('', include(router.urls)),
    path('user/user_goal/goals_by_category/', views.UserGoalViewSet.as_view({'get': 'suggest_goals'}),
         name='goals_by_category'),
    # path('', include(user_profiles_router.urls))
]