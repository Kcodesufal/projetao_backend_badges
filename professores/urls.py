from rest_framework.routers import DefaultRouter

from professores.views.universidade import UniversidadeViewSet
from professores.views.professor import ProfessorViewSet

router = DefaultRouter()
router.register(r'universidades', UniversidadeViewSet, basename='universidade')
router.register(r'', ProfessorViewSet, basename='professor')

urlpatterns = router.urls
