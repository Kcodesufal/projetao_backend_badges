from rest_framework.routers import DefaultRouter

from ongs.views.ong import OngViewSet
from ongs.views.avaliacao import AvaliacaoOngViewSet

router = DefaultRouter()
router.register(r'avaliacoes', AvaliacaoOngViewSet, basename='avaliacao-ong')
router.register(r'', OngViewSet, basename='ong')

urlpatterns = router.urls
