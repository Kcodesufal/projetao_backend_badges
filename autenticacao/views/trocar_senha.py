from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from autenticacao.serializers.trocar_senha import TrocarSenhaSerializer


class TrocarSenhaView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=TrocarSenhaSerializer, responses={200: None})
    def post(self, request):
        serializer = TrocarSenhaSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Senha alterada com sucesso.'}, status=status.HTTP_200_OK)
