from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from estudantes.models.estudantes import Estudante
from estudantes.models.estudantes_turmas import EstudanteTurma
from estudantes.permissions import IsEstudante
from estudantes.serializers.inscricao import (
    InscricaoTurmaSerializer,
    InscricaoDetalheSerializer,
    AtualizarStatusSerializer,
)
from turmas.models.turmas_professor import TurmaProfessor
from turmas.permissions import IsProfessor


@extend_schema_view(
    list=extend_schema(responses={200: InscricaoDetalheSerializer(many=True)}),
    retrieve=extend_schema(responses={200: InscricaoDetalheSerializer}),
    create=extend_schema(request=InscricaoTurmaSerializer, responses={201: InscricaoDetalheSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class InscricaoTurmaViewSet(
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
            return [IsEstudante()]
        if self.action == 'atualizar_status':
            return [IsProfessor()]
        return super().get_permissions()

    def get_queryset(self):
        return EstudanteTurma.objects.select_related(
            'estudante__usuario',
            'turma__universidade',
        ).all()

    def get_serializer_class(self):
        if self.action == 'create':
            return InscricaoTurmaSerializer
        if self.action == 'atualizar_status':
            return AtualizarStatusSerializer
        return InscricaoDetalheSerializer

    def create(self, request, *args, **kwargs):
        serializer = InscricaoTurmaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        inscricao = serializer.save()
        return Response(InscricaoDetalheSerializer(inscricao).data, status=status.HTTP_201_CREATED)

    @extend_schema(request=AtualizarStatusSerializer, responses={200: InscricaoDetalheSerializer})
    @action(detail=True, methods=['patch'], url_path='status')
    def atualizar_status(self, request, pk=None):
        inscricao = self.get_object()

        try:
            professor = inscricao.turma.turmas_professor.get(
                professor__usuario=request.user
            ).professor
        except TurmaProfessor.DoesNotExist:
            return Response(
                {'detail': 'Você não é professor desta turma.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AtualizarStatusSerializer(inscricao, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(InscricaoDetalheSerializer(inscricao).data, status=status.HTTP_200_OK)
