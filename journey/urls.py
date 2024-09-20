from django.urls import include, path
from rest_framework_nested import routers

from journey import views

router = routers.DefaultRouter()
router.register("", views.JourneyViewSet, basename="journey")


journey_router = routers.NestedDefaultRouter(router, "", lookup="journey")
journey_router.register("step", views.JourneyStepViewSet, basename="journey-steps")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(journey_router.urls)),
]
