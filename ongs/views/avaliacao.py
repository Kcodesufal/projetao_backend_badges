from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from aplicacoes.models.aplicacao import Aplicacao
from estudantes.models.estudantes import Estudante
from estudantes.models.estudantes_turmas import EstudanteTurma
from ongs.models.avaliacao import AvaliacaoOng
from ongs.models.ong import Ong
from ongs.serializers.avaliacao import AvaliacaoOngSerializer, AvaliarOngSerializer
from projetos.models.projeto import Projeto


@extend_schema_view(
    list=extend_schema(responses={200: AvaliacaoOngSerializer(many=True)}),
    retrieve=extend_schema(responses={200: AvaliacaoOngSerializer}),
)
class AvaliacaoOngViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = AvaliacaoOngSerializer

    def get_queryset(self):
        return AvaliacaoOng.objects.select_related(
            'estudante__usuario',
            'ong',
            'projeto',
        ).all()

    @extend_schema(
        request=AvaliarOngSerializer,
        responses={201: AvaliacaoOngSerializer, 200: AvaliacaoOngSerializer},
    )
    @action(detail=False, methods=['post'], url_path='avaliar')
    def avaliar(self, request):
        try:
            estudante = Estudante.objects.get(usuario=request.user)
        except Estudante.DoesNotExist:
            return Response(
                {'detail': 'Perfil de estudante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AvaliarOngSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            projeto = Projeto.objects.select_related('ong').get(pk=data['projeto_id'])
        except Projeto.DoesNotExist:
            return Response(
                {'detail': 'Projeto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if projeto.status != Projeto.Status.CONCLUIDO:
            return Response(
                {'detail': 'Só é possível avaliar ONGs de projetos concluídos.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        turmas_aceitas = EstudanteTurma.objects.filter(
            estudante=estudante,
            status=EstudanteTurma.Status.ACEITO,
        ).values_list('turma_id', flat=True)

        participou = Aplicacao.objects.filter(
            turma_id__in=turmas_aceitas,
            atividade__projeto=projeto,
            status=Aplicacao.Status.ACEITA,
        ).exists()

        if not participou:
            return Response(
                {'detail': 'Você não possui participação aceita neste projeto.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        avaliacao, created = AvaliacaoOng.objects.update_or_create(
            estudante=estudante,
            projeto=projeto,
            defaults={
                'ong': projeto.ong,
                'nota': data['nota'],
                'comentario': data.get('comentario', ''),
            },
        )

        response_serializer = AvaliacaoOngSerializer(avaliacao)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @extend_schema(responses={200: AvaliacaoOngSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='minhas-avaliacoes')
    def minhas_avaliacoes(self, request):
        try:
            estudante = Estudante.objects.get(usuario=request.user)
        except Estudante.DoesNotExist:
            return Response(
                {'detail': 'Perfil de estudante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        avaliacoes = AvaliacaoOng.objects.filter(
            estudante=estudante
        ).select_related('ong', 'projeto', 'estudante__usuario')

        response_serializer = self.get_serializer(avaliacoes, many=True)
        return Response(response_serializer.data)
