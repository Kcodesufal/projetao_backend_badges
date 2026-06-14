from rest_framework import serializers

from autenticacao.enums.roles import Role
from autenticacao.serializers.usuario import UsuarioSerializer
from ongs.models.ong import Ong


class OngSerializer(serializers.ModelSerializer):
    usuario_detalhes = UsuarioSerializer(source='usuario', read_only=True)

    class Meta:
        model = Ong
        fields = ('id', 'usuario', 'usuario_detalhes', 'cnpj', 'razao_social', 'causa_social', 'avaliacao_media', 'data_criacao')
        read_only_fields = ('id', 'avaliacao_media', 'data_criacao', 'usuario_detalhes')
        extra_kwargs = {
            'usuario': {'write_only': True},
        }

    def validate_usuario(self, value):
        if value.role != Role.ONG:
            raise serializers.ValidationError('O usuário deve ter o perfil de ONG.')
        return value


class AtualizarOngSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ong
        fields = ('razao_social', 'causa_social')
