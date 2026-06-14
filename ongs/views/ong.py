from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from ongs.models.ong import Ong
from ongs.serializers.ong import OngSerializer, AtualizarOngSerializer
from ongs.serializers.avaliacao import AvaliacaoOngSerializer


@extend_schema_view(
    list=extend_schema(responses={200: OngSerializer(many=True)}),
    retrieve=extend_schema(responses={200: OngSerializer}),
    create=extend_schema(request=OngSerializer, responses={201: OngSerializer}),
    partial_update=extend_schema(request=AtualizarOngSerializer, responses={200: OngSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class OngViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Ong.objects.select_related('usuario').all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AtualizarOngSerializer
        return OngSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OngSerializer(instance).data, status=status.HTTP_200_OK)

    @extend_schema(responses={200: AvaliacaoOngSerializer(many=True)})
    @action(detail=True, methods=['get'], url_path='avaliacoes')
    def avaliacoes(self, request, pk=None):
        ong = self.get_object()
        avaliacoes = ong.avaliacoes.select_related(
            'estudante__usuario',
            'projeto',
        ).order_by('-data_avaliacao')
        serializer = AvaliacaoOngSerializer(avaliacoes, many=True)
        return Response(serializer.data)
