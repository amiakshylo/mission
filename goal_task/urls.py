from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register(
    "goal_suggestion", views.GoalSuggestionsViewset, basename="goal_suggestion"
)
router.register('goals', views.GoalViewSet, basename='goals')

urlpatterns = [
    path("", include(router.urls)),
]
