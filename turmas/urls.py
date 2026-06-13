from rest_framework.routers import DefaultRouter

from turmas.views.turma import TurmaViewSet

router = DefaultRouter()
router.register(r'', TurmaViewSet, basename='turma')

urlpatterns = router.urls
