from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from professores.models.professores import Professor
from turmas.models.turmas import Turma
from turmas.models.turmas_professor import TurmaProfessor
from turmas.permissions import IsProfessor
from turmas.serializers.turma import TurmaSerializer, AtualizarTurmaSerializer, MinhasTurmasSerializer
from estudantes.serializers.inscricao import InscricaoDetalheSerializer
from aplicacoes.models.aplicacao import Aplicacao


@extend_schema_view(
    list=extend_schema(responses={200: TurmaSerializer(many=True)}),
    retrieve=extend_schema(responses={200: TurmaSerializer}),
    create=extend_schema(request=TurmaSerializer, responses={201: TurmaSerializer}),
    partial_update=extend_schema(request=AtualizarTurmaSerializer, responses={200: TurmaSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class TurmaViewSet(
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
        if self.action in ('create', 'partial_update', 'destroy', 'minhas_turmas'):
            return [IsProfessor()]
        return super().get_permissions()

    def get_queryset(self):
        return Turma.objects.select_related('universidade').all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AtualizarTurmaSerializer
        if self.action == 'minhas_turmas':
            return MinhasTurmasSerializer
        return TurmaSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        try:
            professor = Professor.objects.get(usuario=request.user)
        except Professor.DoesNotExist:
            return Response({'detail': 'Perfil de professor não encontrado.'}, status=status.HTTP_403_FORBIDDEN)
            
        if not TurmaProfessor.objects.filter(turma=instance, professor=professor).exists():
            return Response({'detail': 'Você não tem permissão para editar esta turma.'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TurmaSerializer(instance).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        try:
            professor = Professor.objects.get(usuario=request.user)
        except Professor.DoesNotExist:
            return Response({'detail': 'Perfil de professor não encontrado.'}, status=status.HTTP_403_FORBIDDEN)
            
        if not TurmaProfessor.objects.filter(turma=instance, professor=professor).exists():
            return Response({'detail': 'Você não tem permissão para excluir esta turma.'}, status=status.HTTP_403_FORBIDDEN)
            
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={200: MinhasTurmasSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='minhas-turmas')
    def minhas_turmas(self, request):
        try:
            professor = Professor.objects.get(usuario=request.user)
        except Professor.DoesNotExist:
            return Response({'detail': 'Perfil de professor não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        ids_turmas = TurmaProfessor.objects.filter(professor=professor).values_list('turma_id', flat=True)
        turmas = Turma.objects.filter(id__in=ids_turmas).select_related('universidade').prefetch_related('turmas_professor')
        serializer = MinhasTurmasSerializer(turmas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: InscricaoDetalheSerializer(many=True)})
    @action(detail=True, methods=['get'], url_path='inscricoes')
    def inscricoes(self, request, pk=None):
        turma = self.get_object()
        user = request.user
        has_access = False

        if user.role == 'professor':
            has_access = TurmaProfessor.objects.filter(turma=turma, professor__usuario=user).exists()
        elif user.role == 'ong':
            has_access = Aplicacao.objects.filter(turma=turma, atividade__projeto__ong__usuario=user, status=Aplicacao.Status.ACEITA).exists()
        elif user.role == 'estudante':
            from estudantes.models.estudantes_turmas import EstudanteTurma
            has_access = EstudanteTurma.objects.filter(turma=turma, estudante__usuario=user, status=EstudanteTurma.Status.ACEITO).exists()
        else:
            has_access = True # Admin ou outros

        if not has_access:
            return Response({'detail': 'Você não tem permissão para visualizar os inscritos desta turma.'}, status=status.HTTP_403_FORBIDDEN)

        inscricoes = turma.inscricoes.select_related('estudante__usuario', 'turma__universidade').all()
        serializer = InscricaoDetalheSerializer(inscricoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: 'Retorna lista de atividades alocadas para a turma'})
    @action(detail=True, methods=['get'], url_path='atividades')
    def atividades(self, request, pk=None):
        turma = self.get_object()
        aplicacoes = Aplicacao.objects.filter(
            turma=turma,
            status=Aplicacao.Status.ACEITA
        ).select_related('atividade__projeto__ong')
        
        resultado = []
        for app in aplicacoes:
            resultado.append({
                'aplicacao_id': app.id,
                'atividade_id': app.atividade.id,
                'atividade_nome': app.atividade.nome,
                'projeto_id': app.atividade.projeto.id,
                'projeto_nome': app.atividade.projeto.nome,
                'ong_nome': app.atividade.projeto.ong.usuario.nome,
                'data_inicio': app.atividade.data_inicio,
                'data_fim': app.atividade.data_fim,
            })
            
        return Response(resultado, status=status.HTTP_200_OK)
