from django.urls import include, path
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('life-sphere', views.LifeSphereViewSet, basename='life-sphere')
router.register('area', views.AreaViewSet, basename='area')

urlpatterns = [
    path('', include(router.urls)),
]


