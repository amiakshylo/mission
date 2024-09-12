from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('onboarding_question', views.OnboardingViewSet, basename='onboarding_question')




urlpatterns = [
    path('', include(router.urls)),

]

