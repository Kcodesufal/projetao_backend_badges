from rest_framework.routers import DefaultRouter

from estudantes.views.estudante import EstudanteViewSet
from estudantes.views.inscricao import InscricaoTurmaViewSet

router = DefaultRouter()
router.register(r'inscricoes', InscricaoTurmaViewSet, basename='inscricao')
router.register(r'', EstudanteViewSet, basename='estudante')

urlpatterns = router.urls
