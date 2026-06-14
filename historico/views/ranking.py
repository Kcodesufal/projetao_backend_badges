from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from estudantes.models.estudantes import Estudante
from historico.models.ranking import RankingEstudante
from historico.serializers.ranking import RankingEstudanteSerializer


@extend_schema_view(
    list=extend_schema(responses={200: RankingEstudanteSerializer(many=True)}),
    retrieve=extend_schema(responses={200: RankingEstudanteSerializer}),
)
class RankingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = RankingEstudanteSerializer

    def get_queryset(self):
        return RankingEstudante.objects.select_related(
            'estudante__usuario',
            'estudante__universidade',
        ).order_by('-total_pontos')

    @extend_schema(responses={200: RankingEstudanteSerializer})
    @action(detail=False, methods=['get'], url_path='meu-ranking')
    def meu_ranking(self, request):
        try:
            estudante = Estudante.objects.get(usuario=request.user)
        except Estudante.DoesNotExist:
            return Response(
                {'detail': 'Perfil de estudante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        ranking, _ = RankingEstudante.objects.get_or_create(estudante=estudante)
        serializer = self.get_serializer(ranking)
        return Response(serializer.data)
