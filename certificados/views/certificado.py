from django.db.models import Sum
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from aplicacoes.models.aplicacao import Aplicacao
from certificados.models.certificado import Certificado
from certificados.serializers.certificado import CertificadoSerializer, EmitirCertificadoSerializer
from estudantes.models.estudantes import Estudante
from estudantes.models.estudantes_turmas import EstudanteTurma
from projetos.models.projeto import Projeto


@extend_schema_view(
    list=extend_schema(responses={200: CertificadoSerializer(many=True)}),
    retrieve=extend_schema(responses={200: CertificadoSerializer}),
)
class CertificadoViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = CertificadoSerializer

    def get_queryset(self):
        return Certificado.objects.select_related(
            'estudante__usuario',
            'estudante__universidade',
            'projeto__ong',
        ).all()

    @extend_schema(responses={200: CertificadoSerializer(many=True)})
    @action(detail=False, methods=['get'], url_path='meus-certificados')
    def meus_certificados(self, request):
        try:
            estudante = Estudante.objects.get(usuario=request.user)
        except Estudante.DoesNotExist:
            return Response(
                {'detail': 'Perfil de estudante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        certificados = Certificado.objects.filter(
            estudante=estudante
        ).select_related('projeto__ong', 'estudante__usuario', 'estudante__universidade')

        serializer = self.get_serializer(certificados, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=EmitirCertificadoSerializer,
        responses={201: CertificadoSerializer, 200: CertificadoSerializer},
    )
    @action(detail=False, methods=['post'], url_path='emitir')
    def emitir(self, request):
        try:
            estudante = Estudante.objects.get(usuario=request.user)
        except Estudante.DoesNotExist:
            return Response(
                {'detail': 'Perfil de estudante não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmitirCertificadoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        projeto_id = serializer.validated_data['projeto_id']

        try:
            projeto = Projeto.objects.get(pk=projeto_id)
        except Projeto.DoesNotExist:
            return Response(
                {'detail': 'Projeto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if projeto.status != Projeto.Status.CONCLUIDO:
            return Response(
                {'detail': 'O certificado só pode ser emitido para projetos concluídos.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        turmas_aceitas = EstudanteTurma.objects.filter(
            estudante=estudante,
            status=EstudanteTurma.Status.ACEITO,
        ).values_list('turma_id', flat=True)

        atividades_participadas = Aplicacao.objects.filter(
            turma_id__in=turmas_aceitas,
            atividade__projeto=projeto,
            status=Aplicacao.Status.ACEITA,
        ).select_related('atividade')

        if not atividades_participadas.exists():
            return Response(
                {'detail': 'Você não possui participação aceita neste projeto.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        carga_horaria = atividades_participadas.aggregate(
            total=Sum('atividade__carga_horaria')
        )['total'] or 0

        certificado, created = Certificado.objects.get_or_create(
            estudante=estudante,
            projeto=projeto,
            defaults={'carga_horaria': carga_horaria},
        )

        response_serializer = CertificadoSerializer(certificado)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
