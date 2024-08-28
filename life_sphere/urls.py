from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('life-sphere', views.LifeSphereViewSet, basename='life-sphere')

urlpatterns = [
    path('', include(router.urls)),
]



