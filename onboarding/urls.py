from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register("user_answer", views.OnboardingViewSet, basename="user_answer")


urlpatterns = [
    path("", include(router.urls)),
]
