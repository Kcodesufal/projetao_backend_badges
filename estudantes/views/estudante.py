from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

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
