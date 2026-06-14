from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from aplicacoes.models.aplicacao import Aplicacao
from aplicacoes.serializers.aplicacao import AplicacaoSerializer, AtualizarStatusAplicacaoSerializer
from ongs.models.ong import Ong
from projetos.permissions import IsOng
from turmas.permissions import IsProfessor


@extend_schema_view(
    list=extend_schema(responses={200: AplicacaoSerializer(many=True)}),
    retrieve=extend_schema(responses={200: AplicacaoSerializer}),
    create=extend_schema(request=AplicacaoSerializer, responses={201: AplicacaoSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class AplicacaoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action == 'create':
            return [IsProfessor()]
        if self.action == 'atualizar_status':
            return [IsOng()]
        return super().get_permissions()

    def get_queryset(self):
        return Aplicacao.objects.select_related(
            'professor__usuario',
            'turma',
            'atividade__projeto__ong',
        ).all()

    def get_serializer_class(self):
        if self.action == 'atualizar_status':
            return AtualizarStatusAplicacaoSerializer
        return AplicacaoSerializer

    @extend_schema(request=AtualizarStatusAplicacaoSerializer, responses={200: AplicacaoSerializer})
    @action(detail=True, methods=['patch'], url_path='status')
    def atualizar_status(self, request, pk=None):
        aplicacao = self.get_object()

        try:
            ong = Ong.objects.get(usuario=request.user)
        except Ong.DoesNotExist:
            return Response(
                {'detail': 'Usuário não possui perfil de ONG.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if aplicacao.atividade.projeto.ong != ong:
            return Response(
                {'detail': 'Você não é a ONG responsável por este projeto.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AtualizarStatusAplicacaoSerializer(aplicacao, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AplicacaoSerializer(aplicacao).data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: AplicacaoSerializer})
    @action(detail=True, methods=['post'], url_path='rejeitar-estudante')
    def rejeitar_estudante(self, request, pk=None):
        aplicacao = self.get_object()

        try:
            ong = Ong.objects.get(usuario=request.user)
        except Ong.DoesNotExist:
            return Response(
                {'detail': 'Usuário não possui perfil de ONG.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if aplicacao.atividade.projeto.ong != ong:
            return Response(
                {'detail': 'Você não é a ONG responsável por este projeto.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        estudante_id = request.data.get('estudante_id')
        if not estudante_id:
            return Response({'detail': 'estudante_id é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        aplicacao.estudantes_rejeitados.add(estudante_id)
        return Response(AplicacaoSerializer(aplicacao).data, status=status.HTTP_200_OK)
