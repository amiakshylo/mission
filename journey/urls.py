from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('journey', views.JourneyViewSet, basename='journey')

urlpatterns = [
    path('', include(router.urls)),
]
