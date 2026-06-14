from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from projetos.models.projeto import Projeto
from projetos.permissions import IsOng
from projetos.serializers.projeto import ProjetoSerializer, AtualizarProjetoSerializer
from estudantes.serializers.inscricao import InscricaoDetalheSerializer
from aplicacoes.models.aplicacao import Aplicacao
from estudantes.models.estudantes_turmas import EstudanteTurma


@extend_schema_view(
    list=extend_schema(responses={200: ProjetoSerializer(many=True)}),
    retrieve=extend_schema(responses={200: ProjetoSerializer}),
    create=extend_schema(request=ProjetoSerializer, responses={201: ProjetoSerializer}),
    partial_update=extend_schema(request=AtualizarProjetoSerializer, responses={200: ProjetoSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class ProjetoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.action in ('create', 'partial_update', 'destroy'):
            return [IsOng()]
        return super().get_permissions()

    def get_queryset(self):
        return Projeto.objects.select_related('ong').prefetch_related('atividades').all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AtualizarProjetoSerializer
        return ProjetoSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProjetoSerializer(instance).data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: 'Retorna lista de estudantes na equipe'})
    @action(detail=True, methods=['get'], url_path='equipe')
    def equipe(self, request, pk=None):
        projeto = self.get_object()
        
        aplicacoes = Aplicacao.objects.filter(
            atividade__projeto=projeto, 
            status=Aplicacao.Status.ACEITA
        ).prefetch_related('estudantes_rejeitados', 'turma', 'atividade')
        
        resultado = []
        for app in aplicacoes:
            rejeitados_ids = set(app.estudantes_rejeitados.values_list('id', flat=True))
            inscricoes = EstudanteTurma.objects.filter(
                turma=app.turma,
                status=EstudanteTurma.Status.ACEITO
            ).exclude(
                estudante_id__in=rejeitados_ids
            ).select_related('estudante__usuario', 'turma__universidade')
            
            for insc in inscricoes:
                resultado.append({
                    'id': insc.id,
                    'estudante': insc.estudante.id,
                    'estudante_nome': insc.estudante.usuario.nome,
                    'turma': insc.turma.id,
                    'turma_nome': insc.turma.nome,
                    'universidade_nome': insc.turma.universidade.nome,
                    'atividade': app.atividade.id,
                    'atividade_nome': app.atividade.nome,
                    'aplicacao_id': app.id
                })
        
        return Response(resultado, status=status.HTTP_200_OK)
