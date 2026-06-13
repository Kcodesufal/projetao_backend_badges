from rest_framework.routers import DefaultRouter

from aplicacoes.views.aplicacao import AplicacaoViewSet

router = DefaultRouter()
router.register(r'', AplicacaoViewSet, basename='aplicacao')

urlpatterns = router.urls
