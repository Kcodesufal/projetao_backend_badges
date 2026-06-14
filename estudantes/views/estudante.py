from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action

from estudantes.models.estudantes import Estudante
from estudantes.serializers.estudante import EstudanteSerializer, AtualizarEstudanteSerializer


@extend_schema_view(
    list=extend_schema(responses={200: EstudanteSerializer(many=True)}),
    retrieve=extend_schema(responses={200: EstudanteSerializer}),
    create=extend_schema(request=EstudanteSerializer, responses={201: EstudanteSerializer}),
    partial_update=extend_schema(request=AtualizarEstudanteSerializer, responses={200: EstudanteSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class EstudanteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Estudante.objects.select_related('usuario', 'universidade').all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AtualizarEstudanteSerializer
        return EstudanteSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(EstudanteSerializer(instance).data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: 'Retorna lista de atividades do estudante'})
    @action(detail=False, methods=['get'], url_path='minhas-atividades')
    def minhas_atividades(self, request):
        try:
            estudante = Estudante.objects.get(usuario=request.user)
        except Estudante.DoesNotExist:
            return Response({'detail': 'Perfil de estudante não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
        from aplicacoes.models.aplicacao import Aplicacao
        from estudantes.models.estudantes_turmas import EstudanteTurma
        
        turmas_aceitas_ids = EstudanteTurma.objects.filter(
            estudante=estudante, status=EstudanteTurma.Status.ACEITO
        ).values_list('turma_id', flat=True)
        
        aplicacoes = Aplicacao.objects.filter(
            turma_id__in=turmas_aceitas_ids,
            status=Aplicacao.Status.ACEITA
        ).exclude(
            estudantes_rejeitados=estudante
        ).select_related('atividade__projeto__ong', 'turma')
        
        resultado = []
        for app in aplicacoes:
            resultado.append({
                'aplicacao_id': app.id,
                'atividade_id': app.atividade.id,
                'atividade_nome': app.atividade.nome,
                'projeto_id': app.atividade.projeto.id,
                'projeto_nome': app.atividade.projeto.nome,
                'ong_nome': app.atividade.projeto.ong.razao_social,
                'turma_nome': app.turma.nome,
                'data_inicio': app.atividade.data_inicio,
                'data_fim': app.atividade.data_fim,
            })
            
        return Response(resultado, status=status.HTTP_200_OK)
