from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from estudantes.models.estudantes import Estudante
from historico.models.historico import HistoricoEstudante
from historico.serializers.historico import HistoricoEstudanteSerializer


@extend_schema_view(
    list=extend_schema(responses={200: HistoricoEstudanteSerializer(many=True)}),
    retrieve=extend_schema(responses={200: HistoricoEstudanteSerializer}),
)
class HistoricoViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = HistoricoEstudanteSerializer

    def get_queryset(self):
        return HistoricoEstudante.objects.select_related(
            'estudante__usuario',
            'projeto',
        ).all()

    @extend_schema(responses={200: HistoricoEstudanteSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='meu-historico')
    def meu_historico(self, request):
        try:
            estudante = Estudante.objects.get(usuario=request.user)
        except Estudante.DoesNotExist:
            return Response(
                {'detail': 'Perfil de estudante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        historico = HistoricoEstudante.objects.filter(
            estudante=estudante
        ).select_related('projeto').order_by('-data_registro')

        serializer = self.get_serializer(historico, many=True)
        return Response(serializer.data)
