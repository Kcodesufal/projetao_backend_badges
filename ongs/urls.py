from rest_framework.routers import DefaultRouter

from ongs.views.ong import OngViewSet

router = DefaultRouter()
router.register(r'', OngViewSet, basename='ong')

urlpatterns = router.urls
