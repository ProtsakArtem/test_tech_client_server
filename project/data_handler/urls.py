from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataRecordViewSet

router = DefaultRouter()
router.register(r'datarecords', DataRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
