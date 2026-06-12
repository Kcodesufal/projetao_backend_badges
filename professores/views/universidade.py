from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from professores.models.universidades import Universidade
from professores.serializers.universidade import UniversidadeSerializer, AtualizarUniversidadeSerializer


@extend_schema_view(
    list=extend_schema(responses={200: UniversidadeSerializer(many=True)}),
    retrieve=extend_schema(responses={200: UniversidadeSerializer}),
    create=extend_schema(request=UniversidadeSerializer, responses={201: UniversidadeSerializer}),
    partial_update=extend_schema(request=AtualizarUniversidadeSerializer, responses={200: UniversidadeSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class UniversidadeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Universidade.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AtualizarUniversidadeSerializer
        return UniversidadeSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UniversidadeSerializer(instance).data, status=status.HTTP_200_OK)
