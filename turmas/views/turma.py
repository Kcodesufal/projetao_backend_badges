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
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(TurmaSerializer(instance).data, status=status.HTTP_200_OK)

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
        inscricoes = turma.inscricoes.select_related('estudante__usuario', 'turma__universidade').all()
        serializer = InscricaoDetalheSerializer(inscricoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
