from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from atividades.models.atividade import Atividade
from atividades.serializers.atividade import AtividadeSerializer, AtualizarAtividadeSerializer
from projetos.permissions import IsOng


@extend_schema_view(
    list=extend_schema(responses={200: AtividadeSerializer(many=True)}),
    retrieve=extend_schema(responses={200: AtividadeSerializer}),
    create=extend_schema(request=AtividadeSerializer, responses={201: AtividadeSerializer}),
    partial_update=extend_schema(request=AtualizarAtividadeSerializer, responses={200: AtividadeSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class AtividadeViewSet(
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
        return Atividade.objects.select_related('projeto__ong').all()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AtualizarAtividadeSerializer
        return AtividadeSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AtividadeSerializer(instance).data, status=status.HTTP_200_OK)
