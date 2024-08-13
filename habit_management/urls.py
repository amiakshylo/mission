from django.urls import include, path
from rest_framework_nested import routers

from habit_management import views

router = routers.DefaultRouter()
router.register('user_habit', views.UserHabitViewSet, basename='user_habit')

urlpatterns = [
    path('', include(router.urls)),
]
