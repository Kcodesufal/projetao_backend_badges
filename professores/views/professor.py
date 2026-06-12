from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from professores.models.professores import Professor
from professores.serializers.professor import ProfessorSerializer, AtualizarProfessorSerializer


@extend_schema_view(
    list=extend_schema(responses={200: ProfessorSerializer(many=True)}),
    retrieve=extend_schema(responses={200: ProfessorSerializer}),
    create=extend_schema(request=ProfessorSerializer, responses={201: ProfessorSerializer}),
    partial_update=extend_schema(request=AtualizarProfessorSerializer, responses={200: ProfessorSerializer}),
    destroy=extend_schema(responses={204: None}),
)
class ProfessorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Professor.objects.select_related('usuario', 'universidade').all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AtualizarProfessorSerializer
        return ProfessorSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProfessorSerializer(instance).data, status=status.HTTP_200_OK)
