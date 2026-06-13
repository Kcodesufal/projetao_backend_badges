from rest_framework.routers import DefaultRouter

from atividades.views.atividade import AtividadeViewSet

router = DefaultRouter()
router.register(r'', AtividadeViewSet, basename='atividade')

urlpatterns = router.urls
