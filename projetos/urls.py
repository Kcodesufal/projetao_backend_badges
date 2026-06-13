from rest_framework.routers import DefaultRouter

from projetos.views.projeto import ProjetoViewSet

router = DefaultRouter()
router.register(r'', ProjetoViewSet, basename='projeto')

urlpatterns = router.urls
