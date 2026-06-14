from django.urls import path, include
from rest_framework.routers import DefaultRouter
from badges.views.badge import BadgeViewSet

router = DefaultRouter()
router.register(r'', BadgeViewSet, basename='badge')

urlpatterns = [
    path('', include(router.urls)),
]
