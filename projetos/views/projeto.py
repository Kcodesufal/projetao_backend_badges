from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from projetos.models.projeto import Projeto
from projetos.permissions import IsOng
from projetos.serializers.projeto import ProjetoSerializer, AtualizarProjetoSerializer


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
