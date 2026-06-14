from rest_framework.routers import DefaultRouter

from historico.views.historico import HistoricoViewSet
from historico.views.ranking import RankingViewSet

router = DefaultRouter()
router.register(r'ranking', RankingViewSet, basename='ranking')
router.register(r'', HistoricoViewSet, basename='historico')

urlpatterns = router.urls
