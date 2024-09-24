from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.OnboardingViewSet, basename="onboarding")


urlpatterns = [
    path("", include(router.urls)),
]
