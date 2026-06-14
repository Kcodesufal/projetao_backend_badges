from rest_framework.routers import DefaultRouter

from certificados.views.certificado import CertificadoViewSet

router = DefaultRouter()
router.register(r'', CertificadoViewSet, basename='certificado')

urlpatterns = router.urls
