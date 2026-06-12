from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from autenticacao.models.user import Usuario
from autenticacao.serializers.usuario import UsuarioSerializer


class UsuarioListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UsuarioSerializer(many=True)})
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsuarioRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: UsuarioSerializer})
    def get(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)
