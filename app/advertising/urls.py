from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('devices', views.DeviceViewSet)
router.register('audiences', views.AudienceViewSet)
router.register('advertising', views.AdvertisingViewSet)

app_name = 'advertising'

urlpatterns = [
    path('', include(router.urls))
]
