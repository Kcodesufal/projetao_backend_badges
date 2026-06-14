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
from professores.models.professores import Professor
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
        user = self.request.user
        base_qs = EstudanteTurma.objects.select_related(
            'estudante__usuario',
            'turma__universidade',
        )

        if user.role == 'estudante':
            # Estudante só vê as próprias inscrições
            try:
                estudante = Estudante.objects.get(usuario=user)
                return base_qs.filter(estudante=estudante)
            except Estudante.DoesNotExist:
                return base_qs.none()

        if user.role == 'professor':
            # Professor só vê inscrições das turmas que ele ministra
            try:
                professor = Professor.objects.get(usuario=user)
                turma_ids = TurmaProfessor.objects.filter(
                    professor=professor
                ).values_list('turma_id', flat=True)
                return base_qs.filter(turma_id__in=turma_ids)
            except Professor.DoesNotExist:
                return base_qs.none()

        # ONGs, admins e demais roles vêem tudo
        return base_qs.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return InscricaoTurmaSerializer
        if self.action == 'atualizar_status':
            return AtualizarStatusSerializer
        return InscricaoDetalheSerializer

    def create(self, request, *args, **kwargs):
        serializer = InscricaoTurmaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        estudante = serializer.validated_data['estudante']
        turma = serializer.validated_data['turma']

        # Re-inscrição: se havia recusa anterior, reativa em vez de criar duplicata
        existing_rejected = EstudanteTurma.objects.filter(
            estudante=estudante, turma=turma, status=EstudanteTurma.Status.RECUSADO
        ).first()

        if existing_rejected:
            existing_rejected.status = EstudanteTurma.Status.PRE_APROVADO
            existing_rejected.save(update_fields=['status', 'data_atualizacao'])
            return Response(InscricaoDetalheSerializer(existing_rejected).data, status=status.HTTP_200_OK)

        inscricao = serializer.save()
        return Response(InscricaoDetalheSerializer(inscricao).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role == 'estudante' and instance.status == EstudanteTurma.Status.ACEITO:
            return Response(
                {'detail': 'Você não pode cancelar uma inscrição que já foi aceita. Contate seu professor para ser removido.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

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
